import sys, os # For basic file loading/saving and other stuff
import hashlib # For creating sha256 hashes
import subprocess # For running shell commands
import multiprocessing # For getting number of CPUs


# Auto configuration
linuxdir = sys.argv[1]
config_file = linuxdir + "/.config"
os.environ['SRCARCH'] = 'x86'
os.environ['ARCH'] = 'x86'
os.environ['KERNELVERSION'] = linuxdir

if os.path.isfile(config_file):
    hash = hashlib.sha256(open(config_file, 'rb').read()).hexdigest()
else:
    print("ERROR: No `.config` file was found in the dir " + linuxdir +
        ". You should first create a `.config` file.")
    sys.exit(2)

output_dir = "results/" + linuxdir + "/" + hash + "/"


# Setting output language to english
os.environ['LC_ALL'] = ''
os.environ['LC_MESSAGES'] = ''
os.environ['LC_CTYPE'] = ''
os.environ['LANG'] = ''


# Getting number of cpus
cpu_count = multiprocessing.cpu_count()


# Getting version of gcc
os.makedirs(output_dir + "gcc")
gcc_version = subprocess.Popen(
    "gcc -dumpversion > " + output_dir + "gcc/version",
    shell=True, 
    universal_newlines=True)


# Running make on the kernel
job_count = cpu_count * 2
print("  * Compiling with " + str(job_count) + " jobs")
conf_cmd = subprocess.Popen(
    'make -S -j' + str(job_count),
    shell=True,
    stdout=open(output_dir + "gcc/stdout", 'a'),
    stderr=open(output_dir + "gcc/stderr", 'a'),
    universal_newlines=True,
    cwd=linuxdir)
conf_cmd.communicate()


