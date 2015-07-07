import sys, os
import json
import re
import hashlib
#import pymysql
import mysql.connector


# Error catching and usage
if len(sys.argv) <= 1:
    print("Error: no directory given")
    print("Usage: " + sys.argv[0] + " <linux src dir>")
    sys.exit(1)


noconfig = False
if len(sys.argv) == 3:
    if sys.argv[2] == "-noconfig":
        noconfig = True

# Configuration
linuxdir = sys.argv[1]
results_dir = "results/" + linuxdir + "/"
cat_file = "categorized"
nogo_dirs = ['gcc', 'archive'] # Dirs not to follow when looking for bugs

# These can be turned on/off for debugging
do_conf = True
do_bugs = True


# Configuring database
print("  * Connecting to the database")
db = mysql.connector.connect(host='mydb.itu.dk',
    user='elvis_thesis',
    password='linux',
    database='elvis_thesis')

print("      - Setting the cursor")
cursor = db.cursor()


### configurations
# Inserting the config and config hash
if do_conf:
    print("  * Inserting configs")
    if not noconfig:
        for _, dirs, _ in os.walk(results_dir):
            for dir in dirs:
                if not dir in nogo_dirs:
                    config = open(results_dir + dir + "/config", 'r').read()
                    config = re.escape(config)

                    # Reading the linux version
                    version_file = open(results_dir + dir + "/linux_version", 'r')
                    prog_ver = version_file.read()

                    # Reading the exit status
                    es_file = results_dir + dir + "/gcc/exit_status"
                    if os.path.isfile(es_file):
                        exit_status = open(results_dir + dir + "/gcc/exit_status",
                            'r').read()
                    else:
                        exit_status = 3
                    
                    # Reading the configuration warnings/errors
                    ce_file = results_dir + dir + "/conf_errs"
                    if os.path.isfile(ce_file):
                        conf_errs = open(results_dir + dir + "conf_errs", 'r').read()
                    else:
                        conf_errs = None
                        

                    # Inserting configuration into database
                    print("      - Inserting config " + dir[:8])
                    query_config = (
                        "insert ignore into configurations (hash, original, "
                        "exit_status, conf_errs, linux_version)"
                        "values (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\");"
                    )
                    cursor.execute(query_config % (dir, config, exit_status, 
                        conf_errs, prog_ver))


### bugs
# Inserting the categorized warnings
if do_bugs:
    print("  * Inserting the warnings/errors")
    for _, dirs, _ in os.walk(results_dir):
        for dir in dirs:
            if not dir in nogo_dirs:

                # Reading the linux version
                version_file = open(results_dir + dir + "/linux_version", 'r')
                prog_ver = version_file.read()

                # Reading the errors and warnings
                print("     - Reading stderr " + dir[:8])
                stderr_file_path = results_dir + dir + "/categorized"
                stderr_file = open(stderr_file_path, 'r').read()
                json_file = json.loads(str(stderr_file))
                for line in json_file:
                    bugtype = line[0]
                    files = line[1]
                    if line[2]:
                        subsystem = line[2][0]
                    else:
                        subsystem = None
                    original = ""
                    for orig_line in line[3]:
                        original += re.escape(orig_line) + "\n"

                    # Creating the bug_id
                    bulk = "%s%s%s%s%s" % (prog_ver, dir, bugtype, str(files), 
                        original)
                    bulk = bulk.encode('ascii')
                    bug_id = hashlib.sha256(bulk).hexdigest()
                    print("         o Created bug_id = " + bug_id[:8])
                    
                    # Submitting the bug
                    query_bug = (
                        "insert ignore into bugs (hash, type, linux_version, config"
                        ", original, subsystem) values"
                        " (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\");"
                    )
                    cursor.execute(query_bug % (bug_id, bugtype, prog_ver, dir, original, subsystem))

                    ### files
                    # Submitting files
                    if files:
                        for file in files:
                            line = None
                                
                            #print("      - Inserting file " + path)
                            query_file = (
                                "insert ignore into files (path, line, bug_id) values " +
                                "(\"%s\", \"%s\", \"%s\");"
                            )
                            cursor.execute(query_file % (file, line, bug_id))


#cursor.execute('insert into types (name, severity) values ("-Wwhat", 2)')
cursor.close()
