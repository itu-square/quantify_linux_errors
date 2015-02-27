import sys
import re


logmd5 = sys.argv[1]
logdir = 'results/' + logmd5
lines = [line.strip() for line in open(logdir + '/buginfo')]

bugs = []
file_names = []

for line in lines:

    if line[:4] == "make":
        continue

    #if not re.search(r"\^", line) == None:
    if line.strip() == "^":
        bugs.append([bugtype, file_names])
        del bugtype
        files = []
        continue

    bugtype_re = re.search(r"\[\-W.*\]", line)
    if not bugtype_re == None:
        bugtype = bugtype_re.group(0)

    filename_re = re.search(r"(\w+\/)*\w+(\.c|\.h|\.o)", line)
    if not filename_re == None:
        file_names.append(filename_re.group(0))

    

for bug in bugs:
    print(bug)

