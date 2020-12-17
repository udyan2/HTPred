# All types of Fundamental Devices. -> AND OR NOT XOR NOR NAND DFF
import enum
import uuid


class FAN(enum.Enum):
    IN = 0
    OUT = 1


class Port:
    __fan = None
    __parent_gate = None
    __uniqueID = None
    __value = None

    def __init__(self, fan, parent_gate):
        self.__fan = fan
        self.__parent_gate = parent_gate
        self.__uniqueID = uuid.uuid4()
        self.__value = 0

    def get_fan(self):
        return self.__fan

    def get_parent_gate(self):
        return self.__parent_gate

    def set_parent_gate(self,parent_gate):
        self.__parent_gate = parent_gate

    def get_unique_id(self):
        return self.__uniqueID

    def get_value(self):
        return self.__value

    def set_value(self, value):
        if value != 1 and value != 0:
            raise Exception("BIT assigned other than 0 and 1")

        self.__value = value
        if self.__fan == FAN.IN:
            self.__parent_gate.operate()


class Gate:
    _inputPins = None
    _outputPins = None
    _uniqueID = None
    _gateName = None
    _gateType = None

    def __init__(self,gate_name):
        self._gateName = gate_name
        self.__uniqueID = uuid.uuid4()
        pass

    def get_inputs(self):
        return self._inputPins

    def get_outputs(self):
        return self._outputPins

    def get_name(self):
        return self._gateName

    def get_type(self):
        return self._gateType

    def get_unique_id(self):
        return self.__uniqueID


# The following are different gates :

class ANDGate(Gate):
    def __init__(self,gate_name):
        super().__init__(gate_name)
        self._inputPins = {'A':[Port(FAN.IN,self)],'B':[Port(FAN.IN,self)]}
        self._outputPins = {'Y':Port(FAN.OUT,self)}
        self._gateType = 'AND'

    def operate(self):
        self._outputPins['Y'].set_value(self._inputPins['A'].get_value() & self._inputPins['B'].get_value())


class ORGate(Gate):
    def __init__(self, gate_name):
        super().__init__(gate_name)
        self._inputPins = {'A': [Port(FAN.IN, self)], 'B': [Port(FAN.IN, self)]}
        self._outputPins = {'Y': Port(FAN.OUT, self)}
        self._gateType = 'OR'

    def operate(self):
        self._outputPins['Y'].set_value(self._inputPins['A'].get_value() | self._inputPins['B'].get_value())


class NOTGate(Gate):
    def __init__(self, gate_name):
        super().__init__(gate_name)
        self._inputPins = {'A': [Port(FAN.IN, self)]}
        self._outputPins = {'Y': Port(FAN.OUT, self)}
        self._gateType = 'NOT'

    def operate(self):
        if self._inputPins['A'].get_value() == 1:
            self._outputPins['Y'].set_value(0)
        elif self._inputPins['A'].get_value() == 0:
            self._outputPins['Y'].set_value(1)


class XORGate(Gate):
    def __init__(self, gate_name):
        super().__init__(gate_name)
        self._inputPins = {'A': [Port(FAN.IN, self)], 'B': [Port(FAN.IN, self)]}
        self._outputPins = {'Y': Port(FAN.OUT, self)}
        self._gateType = 'XOR'

    def operate(self):
        self._outputPins['Y'].set_value(self._inputPins['A'].get_value() ^ self._inputPins['B'].get_value())


class NANDGate(Gate):
    def __init__(self, gate_name):
        super().__init__(gate_name)
        self._inputPins = {'A': [Port(FAN.IN, self)], 'B': [Port(FAN.IN, self)]}
        self._outputPins = {'Y': Port(FAN.OUT, self)}
        self._gateType = 'NAND'

    def operate(self):
        self._outputPins['Y'].set_value(self._inputPins['A'].get_value() & self._inputPins['B'].get_value())

        if self._outputPins['Y'].get_value() == 1:
            self._outputPins['Y'].set_value(0)
        elif self._outputPins['Y'].get_value() == 0:
            self._outputPins['Y'].set_value(1)


class NORGate(Gate):
    def __init__(self, gate_name):
        super().__init__(gate_name)
        self._inputPins = {'A': [Port(FAN.IN, self)], 'B': [Port(FAN.IN, self)]}
        self._outputPins = {'Y': Port(FAN.OUT, self)}
        self._gateType = 'NOR'

    def operate(self):
        self._outputPins['Y'].set_value(self._inputPins['A'].get_value() | self._inputPins['B'].get_value())

        if self._outputPins['Y'].get_value() == 1:
            self._outputPins['Y'].set_value(0)
        elif self._outputPins['Y'].get_value() == 0:
            self._outputPins['Y'].set_value(1)


class XNORGate(Gate):
    def __init__(self, gate_name):
        super().__init__(gate_name)
        self._inputPins = {'A': [Port(FAN.IN, self)], 'B': [Port(FAN.IN, self)]}
        self._outputPins = {'Y': Port(FAN.OUT, self)}
        self._gateType = 'XNOR'

    def operate(self):
        self._outputPins['Y'].set_value(self._inputPins['A'].get_value() ^ self._inputPins['B'].get_value())

        if self._outputPins['Y'].get_value() == 1:
            self._outputPins['Y'].set_value(0)
        elif self._outputPins['Y'].get_value() == 0:
            self._outputPins['Y'].set_value(1)


class DFF(Gate):
    def __init__(self, gate_name):
        super().__init__(gate_name)
        self._inputPins = {'CK': [Port(FAN.IN, self)], 'D': [Port(FAN.IN, self)]}
        self._outputPins = {'Y': Port(FAN.OUT, self)}
        self._gateType = 'DFF'

    def operate(self):
        self._outputPins['Q'].set_value(self._inputPins['D'].get_value())
