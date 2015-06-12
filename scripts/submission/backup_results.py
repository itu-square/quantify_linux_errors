import os, sys
import shutil


# Error catching
if len(sys.argv) < 2:
    print("Error: No second argument given.")
    print("Usage: python " + sys.argv[0] + " <linux src dir>")
    sys.exit(1)

# Configuration 
prog_ver = sys.argv[1]
results_dir = "results/" + prog_ver + "/"
archive_dir = "archive/"
nogo_dirs = ['gcc', 'archive']


if not os.path.isdir(archive_dir):
    os.makedirs(archive_dir)

# Moves all the dirs to archive
for _, dirs, _ in os.walk(results_dir):
    for dir in dirs:
        if not dir in nogo_dirs:
            print("  * Archiving " + dir[:8])
            shutil.move(results_dir + dir,archive_dir)

