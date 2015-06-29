import sys, os
import subprocess


tarfile = sys.argv[1]
basename = tarfile.split('.tar')[0]
FNULL = open(os.devnull, 'w')

# Removing old dir
if os.path.isdir(basename):
    print("  * Removing directory " + basename)
    rm_p = subprocess.Popen("rm -r " + basename, stdout=FNULL, shell=True)
    rm_p.communicate()
    

# Untarring
print("  * untarring " + tarfile)
untar_p = subprocess.Popen("tar xvf " + tarfile, stdout=FNULL, shell=True)
untar_p.communicate()

