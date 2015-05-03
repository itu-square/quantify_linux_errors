import sys, re, os, random
import kconfiglib


# Usage:
if len(sys.argv) < 3:
    print "Usage: python2 get_minimum.py <kernel dir> <arch>"
    sys.exit(0)

# Setting system environment variables
dirname = sys.argv[1]
os.environ["SRCARCH"] = sys.argv[2]
os.environ["ARCH"] = sys.argv[2]
os.environ["KERNELVERSION"] = dirname[6:]

# Auto configuration
kconfig_name = "Kconfig"
allno = kconfiglib.Config(dirname+"/"+kconfig_name, dirname)
allno.load_config("scripts/gnf/allnoconfig")


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



