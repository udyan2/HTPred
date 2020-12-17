import Module
import module_supplier


class Creator:
    __dir = None
    __file_path = None
    __modules = None
    __main_module = None
    __supplier = None

    def __init__(self, file_path, cell_dir, main_module=None):
        self.__dir = cell_dir
        self.__file_path = file_path
        self.__modules = dict()
        self.__main_module = main_module

        input_data = open(self.__file_path, 'r')
        inputS = input_data.read()
        input_data.close()
        self.__parse(inputS)
        self.__supplier = module_supplier.supplier(cell_dir,self.__modules)

    def convert(self):
        if len(self.__modules) == 1:
            self.__main_module = list(self.__modules.keys())[0]

        m = Module.Module(self.__supplier)
        m.parse(self.__modules[self.__main_module])
        return m.get_bench_file()

    def __parse(self, inputS):
        inp = str()
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
                    self.__modules[curr_mod] = t + '\n'
                else:
                    self.__modules[curr_mod] = self.__modules[curr_mod] + t + '\n'

    def print_modules(self):
        for t in self.__modules.keys():
            print(t + ":\n")
            print(self.__modules[t])


