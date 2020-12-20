import Module


class supplier:
    __folder_path = None
    __predefined_modules = None

    def __init__(self, folder_path):
        self.__folder_path = folder_path
        self.__predefined_modules = dict()

    def get_module(self, module_name):
        if self.__predefined_modules is not None and module_name in self.__predefined_modules.keys():
            r = Module.Module(self)
            r.parse(self.__predefined_modules[module_name])
            return r

        try:
            input_data = open(self.__folder_path + module_name + '.txt', 'r')
            inputS = input_data.read()
            input_data.close()

            self.parse(inputS)
            r = Module.Module(self)
            r.parse(self.__predefined_modules[module_name])
            return r

        except ModuleNotFoundError:
            raise Exception('Module not found')

    def parse(self, inputS):
        curr_mod = str()
        for i in inputS.split('\n'):
            t = i.strip()
            if t[:2] == '//' or t == '':
                continue
            else:
                txt = t.split(' ', 1)
                if txt[0] == 'module':
                    i = -1
                    for a in range(len(txt[1])):
                        if txt[1][a] == '(':
                            i = a
                    curr_mod = txt[1][:i]
                    self.__predefined_modules[curr_mod] = t + '\n'
                else:
                    self.__predefined_modules[curr_mod] = self.__predefined_modules[curr_mod] + t + '\n'

    def get_module_header(self, module_name):
        if module_name in self.__predefined_modules.keys():
            head = str()
            for i in self.__predefined_modules[module_name]:
                head += i
                if i == ';':
                    return head

        else:
            input_data = open(self.__folder_path + module_name + '.txt', 'r')
            inputS = input_data.read()
            input_data.close()

            self.add_module(inputS)
            return self.get_module_header(module_name)

    def get_args(self, module_name):
        header = self.get_module_header(module_name)

        arg_begin = -1
        arg_end = -1

        for i in range(len(header)):
            if header[i] == '(':
                arg_begin = i
            elif header[i] == ')':
                arg_end = i

        args = []
        for t in header[arg_begin + 1:arg_end].split(','):
            args.append(t.strip())
        return args

    def get_modules(self):
        return self.__predefined_modules

    def add_module(self, inputS):
        self.parse(inputS)
