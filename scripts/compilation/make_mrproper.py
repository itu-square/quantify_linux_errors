import sys, os
import subprocess

gcc_change = False
# Checking for number of arguments
if len(sys.argv) == 1:
    print("Error: At least one argument needed.")
    print("Usage: python make_mrproper.py <linux src dir> [gcc-alias]")
elif len(sys.argv) == 3:
    gcc_change = True


linuxdir = sys.argv[1]
FNULL = open(os.devnull, 'w')

if gcc_change:
    gcc_ver = sys.argv[2]
    print("  * Setting gcc alias to " + gcc_ver + " and changing the Makefile")

    filein = open(linuxdir + "/Makefile", 'r')
    filedata = filein.read()
    filein.close()
    newdata = filedata.replace("gcc", gcc_ver)
    fileout = open(linuxdir + "/Makefile", 'w')
    fileout.write(newdata)
    fileout.close()


# Creating the config
print("  * Running `make mrproper`")
mrp_p = subprocess.Popen("make mrproper", shell=True, cwd=linuxdir, stdout=FNULL)
mrp_p.communicate()
#print("  * Running `make randconfig` for the first time.")
#rand_p = subprocess.Popen("make randconfig", shell=True, cwd=linuxdir, stdout=FNULL)
#rand_p.communicate()
