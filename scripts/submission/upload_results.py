import sys, os
import json
import pymysql
import base64


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
    db='elvis_thesis')

cursor = db.cursor()



# Getting the config and config hash
for _, dirs, _ in os.walk(results_dir):
    for dir in dirs:
        if not dir in ['gcc', 'archive']:
            config = open(results_dir + dir + "/config", 'r').read().encode('ascii')
            config_b64 = base64.b64encode(config)
            cursor.execute("insert into configurations (hash, original) values ('" + 
                dir + "', '" + 
                config_b64 + "')")



# Getting the categorized warnings


#cursor.execute('insert into types (name, severity) values ("-Wwhat", 2)')
cursor.close()
