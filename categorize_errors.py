import sys
import re


logmd5 = sys.argv[1]
analyzer = sys.argv[2]
logdir = 'results/' + logmd5 + '/' + analyzer
lines = [line.strip() for line in open(logdir + '/buginfo_raw')]

bugs = []
files = []
bugtype = ""

for line in lines:

    if line[:4] == "make":
        continue

    #if not re.search(r"\^", line) == None:
    if line.strip() == "^":
        bugs.append([bugtype, files])
        bugtype = ""
        files = []
        continue

    bugtype_re = re.search(r"\[\-W.*\]", line)
    if not bugtype_re == None:
        bugtype = bugtype_re.group(0)

    filename_re = re.search(r"(\w+\/)*\w+(\.c|\.h|\.o)", line) # `.o` or not?
    if not filename_re == None:
        filename = filename_re.group(0)
    
        lines_cols_re = re.search(r":[0-9]*:[0-9]*(:|,)", line)
        lines_re = re.search(r":[0-9].*(:|,)", line)
        if not lines_cols_re == None:
            lines_cols = lines_cols_re.group(0)
        elif not lines_re == None:
            lines_cols = lines_re.group(0)

        files.append([filename, lines_cols])
    

for bug in bugs:
    print(bug)

