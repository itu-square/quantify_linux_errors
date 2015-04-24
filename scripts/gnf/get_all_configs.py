import sys, re, os, random


class Config():
    def __init__(self, name, type):
        self.name = name
        self.type = type

        self.intrange = [] # should then fill this list with `a..b`.
        self.strings = [] # All entries about possible strings.
        self.hexs = [] # All entries about possible hex values.

    
    def get_name(self):
        return self.name


    def put_intrange(self, a, b):
        for i in range(int(a), int(b)+1):
            self.intrange.append(i)
            

    def put_string(self, string):
        self.strings.append(string)


    def put_hex(self, hex):
        self.hexs.append(hex)


    def get_value(self):
        type = self.type

        if type == "bool":
            value = random.randrange(2)
            if value == 1:
                return "y"
            else:
                return "n"

        elif type == "tristate":
            value = random.randrange(3)
            if value == 1:
                return "y"
            elif value == 2:
                return "m"
            else:
                return "n"

        elif type == "string":
            count = len(self.strings)
            if count == 0:
                return ""
            value = random.randrange(count)
            return self.strings[value]

        elif type == "int":
            count = len(self.intrange)
            if count == 0:
                return ""
            value = random.randrange(count)
            return self.intrange[value]

        elif type == "hex":
            count = len(self.hexs)
            if count == 0:
                return ""
            value = random.randrange(count)
            return self.hexs[value]

        return 


def concat_kconfigs():
    return os.system("python ../permute_kconfig.py ../../linux-3.19")



configs = {}

configA = Config("A", "int")
configA.put_intrange("5", "15")
print(configA.get_value())

#print(concat_kconfigs())

