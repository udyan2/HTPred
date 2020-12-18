import Gates
import bench_session
import uuid


class wire:
    __in = None
    __out = None
    __uniqueID = None

    def __init__(self):
        self.__uniqueID = uuid.uuid4()
        self.__out = []
        pass

    def __operate(self):
        if self.__in is None:
            return
        for i in self.__out:
            i.set_value(self.__in.get_value)

    def set_in(self, in_port):
        self.__in = in_port

    def add_out(self, out_port):
        self.__out.extend(out_port)

    def remove_out(self,out_port):
        self.__out.remove(out_port)

    def get_endpoints(self):
        return self.__in, self.__out

    def get_in(self):
        return self.__in

    def get_out(self):
        return self.__out

    def get_unique_id(self):
        return self.__uniqueID


class Module:
    _Input_Pins = None
    _Output_Pins = None
    _Internal_Wires = None
    _Internal_Gates = None
    _Module_name = None
    _io_pin_name = None
    _supplier = None

    def __init__(self, supplier):
        self._Input_Pins = dict()
        self._Output_Pins = dict()
        self._Internal_Wires = dict()
        self._Internal_Gates = dict()
        self._io_pin_name = []
        self._supplier = supplier

    def parse(self, module_verilog):
        code_lines = module_verilog.split(";")

        for i in code_lines:
            code_line = i.strip()

            line_part = code_line.split(" ", 1)

            if line_part[0] == "module":
                self.onmodulefound(line_part[1])

            elif line_part[0] == "input":
                self.oninputfound(line_part[1])

            elif line_part[0] == "output":
                self.onoutputfound(line_part[1])

            elif line_part[0] == "wire":
                self.onwirefound(line_part[1])

            elif line_part[0].strip() == "endmodule":
                return

            else:
                self.handle_module_integration(code_line)

    def getInputs(self):
        return self._Input_Pins

    def getOutputs(self):
        return self._Output_Pins

    def getWires(self):
        return self._Internal_Wires

    def getInternalGates(self):
        return self._Internal_Gates

    def onmodulefound(self, line):
        brac_open = -1
        brac_close = -1
        for i in range(0, len(line)):
            if line[i] == '(':
                brac_open = i
            elif line[i] == ')':
                brac_close = i

        self.handle_pins(line[brac_open:brac_close + 1])
        self._Module_name = line[0:brac_open]

    def handle_pins(self, args):
        args = args[1: len(args) - 1]
        for i in args.split(','):
            self._io_pin_name.append(i.strip())

    def oninputfound(self, inputpins):
        inputpins = inputpins.split(",")
        for pins in inputpins:
            self._Input_Pins[pins.strip()] = []

    def onoutputfound(self, outputpins):
        outputpins = outputpins.split(",")
        for pins in outputpins:
            self._Output_Pins[pins.strip()] = None

    def onwirefound(self, wire_list):
        wire_list = wire_list.split(',')
        for i in wire_list:
            curr_wire = i.strip()
            if curr_wire in self.getInputs().keys() or curr_wire in self.getOutputs().keys():
                continue
            self._Internal_Wires[curr_wire] = wire()

    def handle_module_integration(self, line):
        parts = line.split(' ', 1)
        module_type = parts[0]

        arg_begin = -1
        arg_end = -1

        for i in range(len(parts[1])):
            if parts[1][i] == '(' and arg_begin == -1:
                arg_begin = i
            elif parts[1][i] == ')':
                arg_end = i

        module_name = parts[1][:arg_begin]

        arg_list = parts[1][arg_begin + 1:arg_end]
        (mappings,module_key) = self.get_map_dictionary(arg_list,module_type)

        if self.is_module_primitive(module_type):
            temp_gate = None

            if module_type == 'DFF':
                temp_gate = Gates.DFF(module_name,module_key)
            elif module_type == 'OR':
                temp_gate = Gates.ORGate(module_name,module_key)
            elif module_type == 'NOT':
                temp_gate = Gates.NOTGate(module_name,module_key)
            elif module_type == 'AND':
                temp_gate = Gates.ANDGate(module_name,module_key)
            elif module_type == 'NAND':
                temp_gate = Gates.NANDGate(module_name,module_key)
            elif module_type == 'NOR':
                temp_gate = Gates.NORGate(module_name,module_key)
            elif module_type == 'XOR':
                temp_gate = Gates.XORGate(module_name,module_key)
            elif module_type == 'XNOR':
                temp_gate = Gates.XNORGate(module_name,module_key)
            elif module_type == 'BUFF':
                temp_gate = Gates.BUFF(module_name, module_key)

            self._Internal_Gates[module_name + "_" + str(temp_gate.get_unique_id())] = temp_gate

            for k in mappings.keys():
                if k in temp_gate.get_inputs().keys():
                    if mappings[k] in self._Input_Pins.keys():
                        self._Input_Pins[mappings[k]].extend(temp_gate.get_inputs()[k])
                    elif mappings[k] in self._Internal_Wires.keys():
                        self._Internal_Wires[mappings[k]].add_out(temp_gate.get_inputs()[k])

                elif k in temp_gate.get_outputs().keys():
                    if mappings[k] in self._Output_Pins.keys():
                        self._Output_Pins[mappings[k]] = temp_gate.get_outputs()[k]
                    elif mappings[k] in self._Internal_Wires.keys():
                        self._Internal_Wires[mappings[k]].set_in(temp_gate.get_outputs()[k])

        else:
            internal_module = self._supplier.get_module(module_type)

            for i in internal_module.getInternalGates().keys():
                self._Internal_Gates[internal_module.getInternalGates()[i].get_name() + '_' + str(internal_module.getInternalGates()[i].get_unique_id())] = internal_module.getInternalGates()[i]

            for i in internal_module.getWires().keys():
                self._Internal_Wires[i + "_" + str(internal_module.getWires()[i].get_unique_id())] = internal_module.getWires()[i]

            for k in mappings.keys():
                if k in internal_module.getInputs().keys():
                    if mappings[k] in self._Input_Pins.keys():
                        self._Input_Pins[mappings[k]].extend(internal_module.getInputs()[k])
                    elif mappings[k] in self._Internal_Wires.keys():
                        self._Internal_Wires[mappings[k]].add_out(internal_module.getInputs()[k])

                elif k in internal_module.getOutputs().keys():
                    if mappings[k] in self._Output_Pins.keys():
                        self._Output_Pins[mappings[k]] = internal_module.getOutputs()[k]
                    elif mappings[k] in self._Internal_Wires.keys():
                        self._Internal_Wires[mappings[k]].set_in(internal_module.getOutputs()[k])

    def get_map_dictionary(self, arg_list,module_name):
        mappings = dict()
        ordered_args = None
        args = arg_list.split(",")

        itr = 0
        for arg in args:
            arg = arg.strip()

            if arg.find('.') == -1:
                if ordered_args is None:
                    ordered_args = self._supplier.get_args(module_name)
                mappings[ordered_args[itr]] = arg

            else:
                if ordered_args is None:
                    ordered_args = []
                value_part = arg[arg.find('(') + 1:arg.find(')')].strip()
                key_part = arg[arg.find('.') + 1:arg.find('(')].strip()
                mappings[key_part] = value_part
                ordered_args.append(key_part)
            itr += 1

        return mappings, ordered_args

    def is_module_primitive(self, module):
        return module in ['AND', 'OR', 'NOT', 'XOR', 'NAND', 'NOR', 'XOR', 'XNOR', 'DFF', 'BUFF']

    def print_module(self):
        print('Module \'' + self._Module_name + '\'', '\n')
        print('Module Info :', '\n')

        print('INPUT PINS\n' + '------------')
        for i in self._Input_Pins.keys():
            print(i + ' ->', self._Input_Pins[i])
        print()

        print('OUTPUT PINS\n' + '------------')
        for i in self._Output_Pins.keys():
            print(i + ' ->', self._Output_Pins[i])
        print()

        print('WIRES\n' + '------')
        for i in self._Internal_Wires.keys():
            print(i + ' ->', self._Internal_Wires[i], 'Connecting IN of', self._Internal_Wires[i].get_out(),
                  'with OUT of', self._Internal_Wires[i].get_in())
        print()

        print('INTERNAL_GATES\n' + '---------------')
        for i in self.getInternalGates().keys():
            print(
                str(self.getInternalGates()[i]) + " ->" + self.getInternalGates()[i].get_name() + '----> INPUT_PINS [',
                end='')
            for j in self.getInternalGates()[i].get_inputs().keys():
                print('\'' + j + '\': ' + str(self.getInternalGates()[i].get_inputs()[j][0]), end=' ')
            print('] OUTPUT_PINS [', end='')
            for j in self.getInternalGates()[i].get_outputs().keys():
                print('\'' + j + '\': ' + str(self.getInternalGates()[i].get_outputs()[j]), end=' ')
            print(']')

    def get_bench_file(self):
        output = str()
        output += '//Module name: ' + self._Module_name + '\n\n'

        session = bench_session.bench_session(self, 'I', 'U', 'W')
        mapping = session.get_map()

        for i in self.getInputs().keys():
            output += 'INPUT(' + mapping[self.getInputs()[i][0]] + ')\n'
        output += '\n'

        for i in self.getOutputs().keys():
            output += 'OUTPUT(' + mapping[self.getOutputs()[i]] + ')\n'
        output += '\n'

        for i in self.getInternalGates().keys():
            output += mapping[self.getInternalGates()[i].get_outputs()[list(self.getInternalGates()[i].get_outputs())[0]]] + ' = ' + self.getInternalGates()[i].get_type() + '('
            pin_keys = list(self.getInternalGates()[i].get_inputs().keys())
            for pins_i in range(len(pin_keys)):
                output += mapping[self.getInternalGates()[i].get_inputs()[pin_keys[pins_i]][0]]
                if pins_i != len(self.getInternalGates()[i].get_inputs().keys()) - 1:
                    output += ','
            output += ')\n'

        return output
