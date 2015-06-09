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
    "./scripts/kconfig/conf --randconfig Kconfig",
    cwd=linuxdir,
    shell=True, 
    stderr=subprocess.PIPE, 
    stdout=FNULL,
    universal_newlines=True)
conf_errs = conf_cmd.stderr.read()

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
