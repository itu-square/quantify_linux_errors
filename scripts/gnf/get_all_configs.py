import sys, re, os, random
import subprocess
import kconfiglib


dirname = "linux-3.19/"
kconfig_name = "Kconfig_concat"
feature_model = kconfiglib.Config(dirname+kconfig_name, dirname)

types = ["unknown", "bool", "tristate", "string", "hex", "int"]
output = {}

for feature in feature_model:
    type = types[feature.type]
    
    if type == "bool":
        value = random.randrange(2)
        if value == 1:
            output[feature.name] = 'y'
        else:
            output[feature.name] = 'n'

    elif type == "tristate":
        value = random.randrange(3)
        if value == 1:
            output[feature.name] = 'y'
        elif value == 2:
            output[feature.name] = 'm'
        else:
            output[feature.name] = 'n'

    if type == "string":
        strings = []
        value = ""
        exprs = feature.def_exprs
        for v, e in exprs:
            strings.append(v)

        if len(strings) > 0:
            rnd = random.randrange(len(strings))
            value = strings[rnd]
        output[feature.name] = value


for feature in feature_model:
    if feature.type == 3:
        print feature.name
        exprs = feature.def_exprs
        for v, e in exprs:
            print "   " + v

sys.exit(1)

for feature in output:
    print feature + "=" + output[feature]





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


        if type == "string":
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
    return os.popen("python ../permute_kconfig.py ../../" + dirname).readlines()


#lines = concat_kconfigs()
#print(lines[0].rstrip())


#print(concat_kconfigs())

