import sys, os
import json
import pymysql
import base64
import re


# Error catching and usage
if len(sys.argv) <= 1:
    print("Error: no directory given")
    print("Usage: " + sys.argv[0] + " <linux src dir>")
    sys.exit(2)

# Configuration
prog_ver = sys.argv[1]
results_dir = "results/" + prog_ver + "/"
cat_file = "categorized"


# Configuring database
db = pymysql.connect(host='mysql.itu.dk',
    user='elvis_thesis',
    passwd='linux',
    db='elvis_thesis',
    charset='utf8')

cursor = db.cursor()



# Getting the config and config hash
for _, dirs, _ in os.walk(results_dir):
    for dir in dirs:
        if not dir in ['gcc', 'archive']:
            config = open(results_dir + dir + "/config", 'r').read()
            config = re.escape(config)
            #config_b64 = base64.b64encode(config)
            
            # Inserting configuration into database
            #values = dir + ", " + re.escape(str(config))
            query = "insert into configurations (hash, original) values (\"%s\", \"%s\");"
            print(query % (dir, dir))
            cursor.execute(query % (dir, config))


# Getting the categorized warnings


#cursor.execute('insert into types (name, severity) values ("-Wwhat", 2)')
cursor.close()
