import sys, re, os, random, errno
import shutil
import kconfiglib


# Make sure that the kernel source dir is clean.


#################
# Configuration #
#################
nu_configs = 10000
output_dir = "/temp/gnf/" # Remember trailing slash (/)
allnoconfigs_dir = "scripts/gnf/allnoconfigs/"


# Auto configuration
string_debug = False
doscramble = True
onlybool = False
debugging = False


# Usage
if len(sys.argv) < 3:
    print ""
    print "Usage: python2 generate_n_filter.py <kernel dir> <arch> [-[s|n]]"
    print "  -s    Will output all the string symbols and their possible values"
    print "  -n    Will only take the allnoconfig. Used for debugging this script."
    print "  -b    Will only set boolean values. All tristates, ints, strings, hexes"
    print "        Will be set to # FOO is not set."
    print "  -d    Debugging on a toy example. Should be a file ToyConfig in script dir."
    print ""
    sys.exit(1)
elif len(sys.argv) > 3:
    if sys.argv[3] == "-s":
        string_debug = True
    if sys.argv[3] == "-n":
        doscramble = False
    if sys.argv[3] == "-b":
        onlybool = True
    if sys.argv[3] == "-d":
        debugging = True

# Auto configuration 2
dirname = sys.argv[1]
dirnamesplit = dirname.split("-")
version = dirnamesplit[len(dirnamesplit)-1]
arch = sys.argv[2]

kconfig_dir = dirname
kconfig_name = dirname + "/Kconfig"
toyconfig_dir = os.getcwd() + "/scripts/gnf/"
toyconfig = os.getcwd() + "/scripts/gnf/ToyConfig"

if debugging:
    shutil.copyfile(kconfig_name, kconfig_name + ".orig")
    shutil.copyfile(toyconfig, kconfig_name)

min_k_file = allnoconfigs_dir + arch + "_allnoconfig"


# Setting system environment variables
os.environ["SRCARCH"] = arch
os.environ["ARCH"] = arch
os.environ["KERNELVERSION"] = version


# Creating output_dir if not there.
try:
    os.makedirs(output_dir)
except OSError as exc:
    if exc.errno == errno.EEXIST and os.path.isdir(output_dir):
        pass
    else: raise
    

############################
# Loading the Kconfig tree #
############################
feature_model = kconfiglib.Config(kconfig_name, dirname)

# Loading the allnoconfig #
min_k_dict = {}
if not debugging:
    min_k = open(min_k_file)
    min_k = [i.strip().split("=") for i in min_k]
    for key, value in min_k:
        min_k_dict[key] = value 

types = ["unknown", "bool", "tristate", "string", "hex", "int"]
yesno = ['y', 'n']

# This will take all the features NOT in the allnoconfig, and randomize their
# values. Many of the configurations will be invalid.
def scramble(fm):
    output = {}
    skips = ['SRCARCH', 'ARCH', 'KERNELVERSION']

    for f in min_k_dict:
        output[f] = min_k_dict[f]
    choices_taken = []
    counter_min_k = 0

    for feature in fm:
            

        if feature.name in skips:
            continue

        inallno = False
        value = ""

        if feature.get_name() in output:
            continue

        type = types[feature.type]
        ischoice = feature.is_choice_symbol()

        if onlybool:
            if not ischoice and type == "bool":
                output[feature.name] = yesno[random.randrange(2)]
                continue



        if ischoice:
            choice = feature.get_parent()
            choices = choice.get_symbols()

            for choice in choices:
                if choice.name in min_k_dict:
                    inallno = True
                    break

            if inallno: 
                output[feature.name] = "n"
                continue

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
            #print(feature.get_name() + " is bool")
            value = random.randrange(2)
            if value == 1:
                output[feature.name] = 'y'
            else:
                output[feature.name] = 'n'
            continue

        if type == "tristate":
            #print(feature.get_name() + " is tristate")
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

            # coin toss. 50% =n / 50% =<random default>
            rnd = random.randrange(1)
            if rnd == 1:
                output[feature.name] = "n"
                continue
            
            exprs = feature.def_exprs
            for v, e in exprs:
                strings.append(v)

            if len(strings) > 0:
                rnd = random.randrange(len(strings))
                value = strings[rnd]
            output[feature.name] = "\"" + str(value) + "\""
            continue

        if type == "int":


            # coin toss. 50% =n / 50% =<random default>
            rnd = random.randrange(1)
            if rnd == 1: 
                output[feature.name] = "n"
                continue

            #if feature.name in ["INITRAMFS_ROOT_GID", 'MSNDCLAS_IRQ','MSNDPIN_IRQ','INITRAMFS_ROOT_UID']:
                #print(feature)

            defaults = str(feature).split("\n")
            default = ""
            for count, line in enumerate(defaults):
                if line.strip() == "Default values:":
                    default = defaults[count+1].strip().split()
                    value = default[0].strip("\"")
                    break

            output[feature.name] = str(value)
            continue

        if type == "hex":
            #print(feature)
            defaults = str(feature).split("\n")
            default = ""
            for count, line in enumerate(defaults):
                if line.strip() == "Default values:":
                    default = defaults[count+1].strip().split()
                    default = default[0].strip("\"")
                    break
            output[feature.name] = default
            continue
            



    return output


def fewscramble(fm):
    output = {}
    skips = ['SRCARCH', 'ARCH', 'KERNELVERSION']
    toscramble = 1

    for f in min_k_dict:
        output[f] = min_k_dict[f]
    choices_taken = []
    counter_min_k = 0

    featurecount = 0
    for feature in fm:
        featurecount += 1

    while toscramble > 0:
        r = random.randrange(featurecount)

        count2 = 0
        for feature in fm:
            if count2 == r:
                print(feature)
            count2 += 1

        
        toscramble -= 1


    return output


# Will select everything as =n except for what is in the allnoconfig
# This is only for debugging.
def donotscramble(fm):
    output = min_k_dict
    choices_taken = []
    for feature in fm:

        if feature.get_name() in min_k_dict:
            continue

        output[feature.get_name()] = 'n'


    return output



# Prints all of type string, and their possible values.
if ( string_debug ):
    for feature in feature_model:
        if feature.type == 3:
            print feature.name
            exprs = feature.def_exprs
            for v, e in exprs:
                print "   " + v
    sys.exit(1)


# Writing the .config file
for i in range(0, nu_configs):
    print str(i)
    counter_notin = 0
    thefile = open(output_dir + str(i), 'w')

    if ( doscramble ):
        randconf = scramble(feature_model)
    else:
        randconf = donotscramble(feature_model)
    
    for line in randconf:
        if line in ['SRCARCH']:
            continue
        if randconf[line] in ['y']:
            thefile.write("CONFIG_%s=" % line )
            thefile.write("%s\n" % randconf[line] )
        elif randconf[line] in ['n', 'm']:
            thefile.write("# CONFIG_%s is not set\n" % line)
        elif randconf[line].isdigit():
            thefile.write("CONFIG_%s=" % line )
            thefile.write("%s\n" % randconf[line] )
        elif randconf[line][:2] == "0x":
            thefile.write("CONFIG_%s=" % line )
            thefile.write("%s\n" % randconf[line] )
        else:
            thefile.write("CONFIG_%s=" % line )
            thefile.write("%s\n" % randconf[line] )


if debugging:
    shutil.copyfile(kconfig_name + ".orig", kconfig_name)
