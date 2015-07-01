import sys, os
import hashlib
import subprocess
import re


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

### FIXING SOME MANDATORY FEATURES. (Right now, just one)

# Every other config has CONFIG_STANDALONE=n which means that 
# If there is some firmware, that I need to compile a certain 
# driver, that is not in the kernel source, I will get an Error.
# I don't want to count those, so I just have CONFIG_STANDALONE 
# always =y.

changes = [
    ["# CONFIG_STANDALONE is not set", "CONFIG_STANDALONE=y"],
    ["CONFIG_HAVE_KERNEL_LZ4=y", "# CONFIG_HAVE_KERNEL_LZ4 is not set"],
    ["CONFIG_KERNEL_LZ4=y", "# CONFIG_KERNEL_LZ4 is not set"],
    ["CONFIG_RD_LZ4=y", "# CONFIG_RD_LZ4 is not set"],
    ["CONFIG_ZRAM_LZ4=y", "# CONFIG_ZRAM_LZ4 is not set"],
    ["CONFIG_SQUASHFS_LZ4=y", "# CONFIG_SQUASHFS_LZ4 is not set"],
    ["CONFIG_CRYPTO_LZ4=y", "# CONFIG_CRYPTO_LZ4 is not set"],
    ["CONFIG_CRYPTO_LZ4HC=y", "# CONFIG_CRYPTO_LZ4HC is not set"],
    ["CONFIG_LZ4_COMPRESS=y", "# CONFIG_LZ4_COMPRESS is not set"],
    ["CONFIG_LZ4HC_COMPRESS=y", "# CONFIG_LZ4HC_COMPRESS is not set"],
    ["CONFIG_LZ4_DECOMPRESS=y", "# CONFIG_LZ4_DECOMPRESS is not set"],
    ["CONFIG_DECOMPRESS_LZ4=y", "# CONFIG_DECOMPRESS_LZ4 is not set"],
    ["CONFIG_xx=y", "# CONFIG_xx is not set"],
]

print(config_file)
with open(config_file, 'r') as conf:
    conf_lines = conf.readlines()
with open(config_file, 'w') as conf:
    for line in conf_lines:
        for change in changes:
            if re.match(change[0], line):
                print(line)
                line = re.sub(change[0], change[1], line)
        conf.write(line)



# Finding hash of config
conf_hex = open(config_file, 'rb').read()
hash = hashlib.sha256(conf_hex).hexdigest()
print("      - Hash of `.config` is " + hash[:8])

# Creating output dir
output_dir += hash + "/"
os.makedirs(output_dir)

# Copying config and config errors
subprocess.Popen("cp .config" + " ../" + output_dir + "config",
    cwd=linuxdir,
    shell=True)
with open(output_dir + "conf_errs", 'w') as file:
    file.write(conf_errs)
print("      - Length of config warnings is: " + str(len(conf_errs)))
