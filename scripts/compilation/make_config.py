import sys, os
import hashlib
import subprocess


linuxdir = sys.argv[1]
config_file = linuxdir + "/.config"
output_dir = "results/" + linuxdir + "/"
os.environ['SRCARCH'] = 'x86'
os.environ['ARCH'] = 'x86'
os.environ['KERNELVERSION'] = linuxdir
FNULL = open(os.devnull, 'w')

# Check if `make mrproper` has been run ?? Should I do this?


# Creating `results` dir if not exist
if not os.path.isdir("results"):
    print("  * Creating `results` directory")
    os.makedirs("results")

if not os.path.isdir("results/" + linuxdir):
    print("  * Creating `" + linuxdir + "` directory")

# Creating the config file and getting the error messages
print("  * Running `make randconfig`")
conf_cmd = subprocess.Popen(
    #"./scripts/kconfig/conf --randconfig Kconfig",
    "make randconfig",
    cwd=linuxdir,
    shell=True, 
    stderr=subprocess.PIPE, 
    stdout=FNULL,
    universal_newlines=True)
conf_errs = conf_cmd.stderr.read()

# For gcc version < 4.9 only
# But I am adding it to the code anyways.
# I have to change a line in every config file, otherwise
# half of the configs are invalide, which is a damn waste of time.
#sed_cmd = subprocess.Popen(
    #"sed s/STRONG\=y/STRONG\=n/ .config",
    #shell=True,
    #stderr=FNULL,
    #stdout=FNULL,
    #cwd=linuxdir)
# ELVIS TODO


# Finding hash of config
hash = hashlib.sha256(open(config_file, 'rb').read()).hexdigest()
print("      - Hash of `.config` is " + hash)

# Creating output dir
output_dir += hash + "/"
os.makedirs(output_dir)

# Copying config and config errors
subprocess.Popen("cp .config ../" + output_dir + "config",
    cwd=linuxdir,
    shell=True)
with open(output_dir + "conf_errs", 'w') as file:
    file.write(conf_errs)
print("      - Length of config warnings is: " + str(len(conf_errs)))
