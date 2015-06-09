import sys, os
from subprocess import call


linuxdir = sys.argv[1]

# Check if `make mrproper` has been run ?? Should I do this?


# Creating the config
print("  * Running `make mrproper`")
call("cd " + linuxdir + " && make mrproper &> /dev/null", shell=True)
print("  * Running `make randconfig`")
call("cd " + linuxdir + " && make randconfig &> /dev/null", shell=True)
