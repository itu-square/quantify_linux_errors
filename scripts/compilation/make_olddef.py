import sys, os
import hashlib
import subprocess
import re
import shutil


linuxdir = sys.argv[1]
config_file = linuxdir + "/config"
output_dir = "results/" + linuxdir + "/"
os.environ['SRCARCH'] = 'x86'
os.environ['ARCH'] = 'x86'
os.environ['KERNELVERSION'] = linuxdir
FNULL = open(os.devnull, 'w')

# Finding hash of config that already exists
# This means, that if there is a change in the config in the newer linux, eg.
# some feature is added, then it will not get a new hash of that. This is so
# it is possible to find and match the two runs.

# finding out what the linux_version should be
version_file = open(linuxdir + '/linux_version', 'r')
linux_version = version_file.read()


conf_hex = open(config_file, 'rb').read()
hash = hashlib.sha256(conf_hex).hexdigest()
print("      - Hash of `config` is " + hash[:8])


# Creating `results` dir if not exist
if not os.path.isdir("results"):
    print("  * Creating `results` directory")
    os.makedirs("results")

if not os.path.isdir("results/" + linuxdir):
    print("  * Creating `" + linuxdir + "` directory")



# Creating the config file and getting the error messages
shutil.copyfile(config_file, linuxdir + "/.config")
print("  * Running `make olddefconfig`")
conf_cmd = subprocess.Popen(
    "make olddefconfig",
    cwd=linuxdir,
    shell=True, 
    stderr=subprocess.PIPE, 
    stdout=FNULL,
    universal_newlines=True)
conf_errs = conf_cmd.stderr.read()


# Creating output dir
output_dir += hash + "/"
print("      - Creating dir " + output_dir)
os.makedirs(output_dir)


# Copying config and config errors
subprocess.Popen("cp .config" + " ../" + output_dir + "config",
    cwd=linuxdir,
    shell=True)
with open(output_dir + "conf_errs", 'w') as file:
    file.write(conf_errs)
print("      - Length of config warnings is: " + str(len(conf_errs)))

version_file = open(output_dir + "linux_version", 'w')
version_file.write(linux_version)
