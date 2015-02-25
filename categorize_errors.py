import sys
import re


logmd5 = sys.argv[1]
logdir = 'results/' + logmd5
lines = [line.strip() for line in open(logdir + '/buginfo')]

bugs = []

bugtype = ""
file_names = []
file_line = ""
for line in lines:

    if not re.search(r"\^", line) == None:
        bugs.append([bugtype, file_names])
        bugtype = ""
        file_names = []
        file_line = ""
        continue

    bugtype_re = re.search(r"\[\-W.*\]", line)
    if not bugtype_re == None:
        bugtype = bugtype_re.group(0)

    filename_re = re.search(r"(\w+|\/|_)+(\.c|\.h)", line)
    if not filename_re == None:
        file_names.append(filename_re.group(0))
    #file_re = re.split(":", line)
    #file_line = file_re[1]

    


print(bugs)

