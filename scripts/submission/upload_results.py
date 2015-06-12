import sys, os
import json
import base64
import re
import hashlib
sys.path.append(os.path.relpath('pymysql'))
import pymysql


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
prog_ver = sys.argv[1]
results_dir = "results/" + prog_ver + "/"
cat_file = "categorized"
nogo_dirs = ['gcc', 'archive'] # Dirs not to follow when looking for bugs


# Configuring database
db = pymysql.connect(host='mysql.itu.dk',
    user='elvis_thesis',
    passwd='linux',
    db='elvis_thesis',
    charset='utf8')

cursor = db.cursor()


# Inserting the config and config hash
if not noconfig:
    for _, dirs, _ in os.walk(results_dir):
        for dir in dirs:
            if not dir in nogo_dirs:
                config = open(results_dir + dir + "/config", 'r').read()
                config = re.escape(config)
                
                # Inserting configuration into database
                print("  * Insert conf " + dir[:8])
                query_config = (
                    "insert ignore into configurations (hash, original)"
                    "values (\"%s\", \"%s\");"
                )
                cursor.execute(query_config % (dir, config))


# Inserting the categorized warnings
for _, dirs, _ in os.walk(results_dir):
    for dir in dirs:
        if not dir in nogo_dirs:
            print("  * Reading stderr " + dir[:8])
            stderr_file = open(results_dir + dir + "/categorized", 'r')
            json_file = json.load(stderr_file)
            for line in json_file:
                bugtype = line[0]
                files = line[1]
                original = ""
                for orig_line in line[2]:
                    original += re.escape(orig_line) + "\n"

                # Creating the bug_id
                bulk = "%s%s%s%s" % (dir, bugtype, str(files), original)
                bulk = bulk.encode('ascii')
                bug_id = hashlib.sha256(bulk).hexdigest()
                print("  * Created bug_id = " + bug_id[:8])
                
                # Submitting the bug
                print("      - Inserting bug " + bug_id[:8])
                query_bug = (
                    "insert ignore into bugs (id, type, version, config, "
                    "original) values"
                    " (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\");"
                )
                cursor.execute(query_bug % (bug_id, bugtype, prog_ver, dir, original))

                # Submitting files
                for file in files:
                    path = file[0]
                    line = file[1]
                    #print("      - Inserting file " + path)
                    query_file = (
                        "insert ignore into files (path, line, bug_id) values " +
                        "(\"%s\", \"%s\", \"%s\");"
                    )
                    cursor.execute(query_file % (path, line, bug_id))


#cursor.execute('insert into types (name, severity) values ("-Wwhat", 2)')
cursor.close()
