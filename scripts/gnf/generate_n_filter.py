import sys, re, os, random, errno
import kconfiglib


#################
# Configuration #
#################
nu_configs = 10
output_dir = "/temp/gnf/" # Remember trailing slash (/)
allnoconfigs_dir = "scripts/gnf/allnoconfigs/"


# Auto configuration
string_debug = False
kconfig_name = "Kconfig"


# Usage
if len(sys.argv) < 3:
    print ""
    print "Usage: python2 generate_n_filter.py <kernel dir> <arch> [-s]"
    print "  -s    Will output all the string symbols and their possible values"
    print ""
    sys.exit(1)
elif len(sys.argv) > 3:
    if sys.argv[3] == "-s":
        string_debug = True

# Auto configuration 2
dirname = sys.argv[1]
dirnamesplit = dirname.split("-")
version = dirnamesplit[len(dirnamesplit)-1]
arch = sys.argv[2]
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
feature_model = kconfiglib.Config(dirname+"/"+kconfig_name, dirname)

# Loading the allnoconfig for this architecture #
#os.popen("python2 scripts/gnf/get_minimum_k.py " + dirname + " " + arch + ">" + min_k_file)
min_k = open(min_k_file)
min_k = [i.split("=")[0] for i in min_k]
feature_model.load_config(min_k_file)

types = ["unknown", "bool", "tristate", "string", "hex", "int"]

# This will take all the features NOT in the allnoconfig, and randomize their
# values. Many of the configurations will be invalid.
def scramble(fm):
    output = {}
    choices_taken = []
    for feature in fm:

        # Checks if the feature is in the minimal configuration
        if "CONFIG_"+feature.get_name() in min_k:
            output[feature.name] = feature.get_value()
            continue

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


# Will select everything as =n except for what is in the allnoconfig
# This is only for debugging.
def donotscramble(fm):
    output = {}
    choices_taken = []
    for feature in fm:

        # Checks if the feature is in the minimal configuration
        if "CONFIG_"+feature.get_name() in min_k:
            output[feature.name] = feature.get_value()
            continue

        type = types[feature.type]
        ischoice = feature.is_choice_symbol()
        value = "n"

        if ischoice:
            output[feature.name] = value
            continue
        
        if type == "bool":
            output[feature.name] = value
            continue

        elif type == "tristate":
            output[feature.name] = value
            continue

        if type == "string":
            output[feature.name] = value
            continue

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
    thefile = open(output_dir + str(i), 'w')
    #randconf = scramble(feature_model)
    randconf = donotscramble(feature_model)
    for line in randconf:
        if randconf[line] in ['y', 'm']:
            thefile.write("CONFIG_%s=" % line )
            thefile.write("%s\n" % randconf[line] )
        elif randconf[line] in ['n']:
            continue
        elif randconf[line].isdigit():
            thefile.write("CONFIG_%s=" % line )
            thefile.write("%s\n" % randconf[line] )
        elif randconf[line][:2] == "0x":
            thefile.write("CONFIG_%s=" % line )
            thefile.write("%s\n" % randconf[line] )
        else:
            thefile.write("CONFIG_%s=" % line )
            thefile.write("\"%s\"\n" % randconf[line] )



