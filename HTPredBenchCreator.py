import Module
import module_supplier

# HTPredBenchCreator.Creator v1.0

class Creator:
    __dir = None
    __file_path = None
    __main_module = None
    __supplier = None

    def __init__(self, file_path, cell_dir, main_module=None):
        self.__dir = cell_dir
        self.__file_path = file_path
        self.__main_module = main_module

        self.__supplier = module_supplier.supplier(cell_dir)
        input_data = open(self.__file_path, 'r')
        inputS = input_data.read()
        input_data.close()
        self.__supplier.add_module(inputS)

    def convert(self):
        if len(self.__supplier.get_modules()) == 1:
            self.__main_module = list(self.__supplier.get_modules().keys())[0]

        m = Module.Module(self.__supplier)
        m.parse(self.__supplier.get_modules()[self.__main_module])
        return m.get_bench_file()

    def print_modules(self):
        for t in self.__supplier.get_modules().keys():
            print(t + ":\n")
            print(self.__supplier.get_modules()[t])


