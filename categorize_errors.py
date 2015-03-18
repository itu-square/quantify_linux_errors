import sys, re, os, codecs


result_dir = "results/"
bug_filename = "buginfo_raw"


def is_utf8_file(program, md5sum, analyzer):
    dir = result_dir + program + "/" + md5sum + '/' + analyzer
    bugfile = dir + "/" + bug_filename
    encoding = os.popen("file " + bugfile + "|grep -o ':\ *[a-zA-Z0-9\-_]*'|awk '{print $2}'").readlines()
    return encoding[0].strip()



def get_bugs_from(program, md5sum, analyzer):
    logdir = result_dir + program + "/" + md5sum + '/' + analyzer
    lines = []
    for line in open(logdir + '/' + bug_filename):
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
        

program = sys.argv[1]
dirlist = []
acc_enc = ["UTF", "empty"]

for _, dirs, _ in os.walk(result_dir + program):
    for dir in dirs:
        if not dir == "":
            if not is_utf8_file(program, dir, "gcc") in acc_enc:
                continue
            dirlist.append(dir)

for dir in dirlist:
    print("########  " + dir)
    bugs = get_bugs_from(program, dir, "gcc")
    for bug in bugs:
        pass
        print(bug)
