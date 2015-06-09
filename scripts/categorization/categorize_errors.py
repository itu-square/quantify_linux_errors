import sys, re, os, codecs


# Configuration
stderr_file = "stderr"
prog_ver = sys.argv[1]
results_dir = "results/" + prog_ver

dirlist = []
acc_enc = ["UTF", "empty"]


def is_utf8_file(hash):
    dir = results_dir + "/" + hash + '/gcc/'
    bugfile = dir + stderr_file
    encoding = os.popen("file " + bugfile + "|grep -o ':\ *[a-zA-Z0-9\-_]*'|awk '{print $2}'").readlines()
    return encoding[0].strip()



def get_gcc_warns(hash):
    logdir = results_dir + "/" + hash + '/gcc/'
    lines = []
    for line in open(logdir + '/' + stderr_file):
        line = str(line.strip())
        codecs.encode(line, 'ascii', 'ignore')
        lines.append(line)
    print(lines)

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

        filename_re = re.search(r"([a-zA-Z0-9_\-+,]*\/).*\w+(\.c|\.h|\.o)", line) # `.o` or not?
        if not filename_re == None:
            filename = filename_re.group(0)
        
            lines_cols = ""
            lines_cols_re = re.search(r":[0-9]*:[0-9]*(:|,)", line)
            lines_re = re.search(r":[0-9].*(:|,)", line)
            if not lines_cols_re == None:
                lines_cols = lines_cols_re.group(0)
            elif not lines_re == None:
                lines_cols = lines_re.group(0)

            files.append([filename, lines_cols])

    return bugs
        

def save_warns(hash, bugs):
    fopen = open(results_dir + "/" + hash + "/categorized", "a")
    fopen.write(str(bugs))


# Finds all the dirs (sha256 hashes)
for _, dirs, _ in os.walk(results_dir):
    for dir in dirs:
        if not dir in ['gcc', 'archive']:
            dirlist.append(dir)


# Gets all the bugs from every compilation dir
for dir in dirlist:
    print("  * " + dir)
    bugs = get_gcc_warns(dir)
    save_warns(dir, bugs)
