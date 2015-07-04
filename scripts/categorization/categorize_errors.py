import sys, re, os, codecs
import json


# Error catching and usage
if len(sys.argv) <= 1:
    print("Error: No directory given")
    print("Usage: " + sys.argv[0] + " <linux src dir>")
    sys.exit(2)

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



def get_warns(hash):
    logdir = results_dir + "/" + hash + '/gcc/'

    # Getting the entire file
    lines = []
    for line in open(logdir + stderr_file):
        line = str(line.strip())
        codecs.encode(line, 'ascii', 'ignore')
        lines.append(line)
    
    found_err = False
    output = []
    makemsgs = []
    bug = []
    orig = []
    files = []
    subsystems = []

    # Going through line for line to categorize
    for line in lines:
        
        orig.append(line)
        
        # Files
        wfiles = get_filenames(line)
        if wfiles:
            for wfile in wfiles:
                files.append(wfile)

        # Check if WARNING
        line_re = re.search(r'\[\-W', line)
        if line_re:
            type_re = re.search(r"\[\-W.*\]", line)
            if not type_re == None:
                type = type_re.group(0)
            

            # Grabbing files
            #files = get_filenames(line)

            # Grabbing subsystems
            subsystems = get_subsystem(line)

            # Appending to output
            bug = [type, files, subsystems, orig]
            output.append(bug)

            # resetting
            bug = []
            type = ''
            files = []
            subsystems = []
            orig = []

            continue


        # Check if ERROR
        if line[:4] == 'make':
            found_err = True
            makemsgs.append(line)

            continue

    
    if found_err:
        err_files = []
        err_subsystems = []

        # Puttin the makemsgs into the orig-list
        for makemsg in makemsgs:
            orig.append(makemsg)

        # Grabbing filenames
        for makemsg in orig:
            mfiles = get_filenames(makemsg)
            if mfiles:
                for mfile in mfiles:
                    err_files.append(mfile)

        # Grabbing subsystem
        for makemsg in orig:
            msubs = get_subsystem(makemsg)
            if msubs:
                for msub in msubs:
                    err_subsystems.append(msub)

        bug = ['makeMsg', err_files, err_subsystems, orig]
        output.append(bug)

    return output


def get_subsystem(line):
    subsystems = []
    ss_search = r"[a-zA-Z0-9_]*\/"
    ss = re.search(ss_search, line)
    if ss:
        subsystems.append(ss.group(0))
    return subsystems
    
def get_filenames(line):
    files = []
    lines = []
    lines_cols = ''
    #filename_re = re.search(r"([a-zA-Z0-9_\-+,]*\/).*", line) # `.o` or not?
    #filename_re = re.search(r"^(.*/)?(?:$|(.+?)(?:(\.[^.]*$)|$))", line)
    #search = r"[a-zA-Z0-9\/\._]*[\/\.]+[a-zA-Z0-9\/_]+"
    search = r"[a-zA-Z/_\.0-9]*[\/\.]+[a-zA-Z_0-9]+[a-zA-Z_0-9]*"
    filenames = re.findall(search, line)
    if filenames:
        
        lines_cols = ""
        lines_cols_re = re.search(r":[0-9]*:[0-9]*(:|,)", line)
        lines_re = re.search(r":[0-9]*(:|,)", line)
        if lines_cols_re:
            lines_cols = lines_cols_re.group(0)
        elif not lines_re == None:
            lines_cols = lines_re.group(0)
    else:
        return None

    #return [filenames, lines_cols]
    return filenames
    
        

# Saves the `bugs` list to the `/results/<prg_ver>/hash/categorized` file
def save_warns(hash, bugs):
    fopen = open(results_dir + "/" + hash + "/categorized", "w")
    fopen.write(json.dumps(bugs))
    fopen.close()


# Finds all the dirs (sha256 hashes)
for _, dirs, _ in os.walk(results_dir):
    for dir in dirs:
        if not dir in ['gcc']:
            dirlist.append(dir)


# Gets all the bugs from every compilation dir
for dir in dirlist:
    print("  * " + dir)
    bugs = get_warns(dir)
    save_warns(dir, bugs)


def get_gcc_warns(hash):
    logdir = results_dir + "/" + hash + '/gcc/'
    lines = []
    for line in open(logdir + stderr_file):
        line = str(line.strip())
        codecs.encode(line, 'ascii', 'ignore')
        lines.append(line)

    bugs = []
    files = []
    org_msg = []
    bugtype = ""
    subsystem = None

    for line in lines:

        if line[:4] == "make":
            bugtype = 'makeMsg'
            org_msg.append(line)
            files = get_filenames(line)
            subsystem = get_subsystem(line)
            bugs.append([bugtype, files, org_msg, subsystem])
            bugtype = ''
            files = []
            org_msg = []
            subsystem = None
            continue

        #if not re.search(r"\^", line) == None:
        if line.strip() == "^":
            if bugtype == '':
                bugtype = 'unknown'
            else:
                bugtype = bugtype.strip('[-]')
            bugs.append([bugtype, files, org_msg, subsystem])
            bugtype = ""
            files = []
            org_msg = []
            subsystem = None
            continue

        # Saving the original line
        org_msg.append(line) # The original message

        # Looking for the bugtype
        bugtype_re = re.search(r"\[\-W.*\]", line)
        if not bugtype_re == None:
            bugtype = bugtype_re.group(0)

        # Looking for the files and line numbers
        if get_filenames(line):
            files.append(get_filenames(line))

        # Getting the subsystem
        subsystem = get_subsystem(line)

    return bugs


