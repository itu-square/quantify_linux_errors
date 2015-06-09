import sys, os
import subprocess


linuxdir = sys.argv[1]
FNULL = open(os.devnull, 'w')

# Check if `make mrproper` has been run ?? Should I do this?


# Creating the config
print("  * Running `make mrproper`")
mrp_p = subprocess.Popen("make mrproper", shell=True, cwd=linuxdir, stdout=FNULL)
mrp_p.communicate()
print("  * Running `make randconfig`")
rand_p = subprocess.Popen("make randconfig", shell=True, cwd=linuxdir, stdout=FNULL)
rand_p.communicate()
