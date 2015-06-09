import sys, re, os
import kconfiglib

# Configuration
output_dir = "scripts/gnf/allnoconfigs/"

# Usage:
if len(sys.argv) < 3:
    print "Usage: python2 get_minimum.py <kernel dir> <arch>"
    sys.exit(0)

# Setting system environment variables
arch = sys.argv[2]
dirname = sys.argv[1]
os.environ["SRCARCH"] = arch
os.environ["ARCH"] = arch
os.environ["KERNELVERSION"] = dirname[6:]

# Auto configuration
kconfig_name = "Kconfig"
allno = kconfiglib.Config(dirname+"/"+kconfig_name, dirname)
allno.load_config(output_dir + arch + "_allnoconfig")


def in_allno(name):
    if allno[name].get_user_value() != None:
        if allno[name].get_type() in [3, 4, 5]:
            if not allno[name].get_value() == "":
                return True
        if allno[name].get_type() in [1, 2]:
            if allno[name].get_value() == "y":
                return True
    return False


for i in allno:
    if in_allno(i.get_name()):
        if i.get_type() in [3, 4, 5]:
            print("CONFIG_" + i.get_name() + "=\"" + i.get_value() + "\"")
        else:
            print("CONFIG_" + i.get_name() + "=" + i.get_value())



