import sys, re, os, random
import kconfiglib


# Configuration
nu_configs = 1
output_dir = "/tmp/gnf/" # Remember trailing slash (/)

# Auto configuration
kconfig_name = "Kconfig"
dirname = sys.argv[1]
dirnamesplit = dirname.split("-")
version = dirnamesplit[len(dirnamesplit)-1]


# Usage
if len(sys.arg) < 4:
    print "Usage: python2 generate_n_filter.py <kernel dir> <arch> [-s]"
    print ""
    print "-s  Will output all the string symbols and their possible values"


# Setting system environment variables
os.environ["SRCARCH"] = sys.argv[2]
os.environ["ARCH"] = sys.argv[2]
os.environ["KERNELVERSION"] = version

# Loading the Kconfig tree
feature_model = kconfiglib.Config(dirname+"/"+kconfig_name, dirname)

types = ["unknown", "bool", "tristate", "string", "hex", "int"]

def scramble(fm):
    output = {}
    choices_taken = []
    for feature in fm:
        type = types[feature.type]
        ischoice = feature.is_choice_symbol()
        if ischoice:
            choice = feature.get_parent()
            choices = choice.get_symbols()
            rnd = random.randrange(len(choices))
            if choice in choices_taken:
                value = "n"
            elif rnd == 0:
                value = "y"
                choices_taken.append(choice)
            else:
                value = "n"
            output[feature.name] = value
            continue
        
        if type == "bool":
            value = random.randrange(2)
            if value == 1:
                output[feature.name] = 'y'
            else:
                output[feature.name] = 'n'
            continue

        elif type == "tristate":
            value = random.randrange(3)
            if value == 1:
                output[feature.name] = 'y'
            elif value == 2:
                output[feature.name] = 'm'
            else:
                output[feature.name] = 'n'
            continue

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
            continue


    return output



# Prints all of type string, and their possible values.
if ( sys.argv[3] == "-s" ):
    for feature in feature_model:
        if feature.type == 3:
            print feature.name
            exprs = feature.def_exprs
            for v, e in exprs:
                print "   " + v
    sys.exit(1)


# Writing the .config file
for i in range(0, nu_configs):
    thefile = open(output_dir + str(i), 'w')
    randconf = scramble(feature_model)
    for line in randconf:
        thefile.write("CONFIG_%s=" % line )
        if randconf[line] in ['y', 'n', 'm']:
            thefile.write("%s\n" % randconf[line] )
        else:
            thefile.write("\"%s\"\n" % randconf[line] )



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

