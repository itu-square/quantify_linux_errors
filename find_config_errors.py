import sys, math, os


# Configuration
rootdir = "randconfig_results/"


def extract_errors(dir):
    file = rootdir + dir + "/stderr.log"
    lines = [line.strip() for line in open(file)]
    errors = []

    for line in lines:
        if line[:7] == "warning":
            errors.append(line[9:])

    return errors


kconf_errors = {}
dirlist = []

print("Reading dirs")
for _, dirs, _ in os.walk(rootdir):
    for dir in dirs:
        if not dir == "":
            dirlist.append(dir)


print("Going through the list")

for counter, dir in enumerate(dirlist):
    if counter%100 == 0:
        print(counter)

    errors = extract_errors(dir)

    if not errors:
        continue

    for error in errors:
        if error in kconf_errors:
            kconf_errors[error] += 1
        else:
            kconf_errors[error] = 1

for error in kconf_errors:
    print(str(kconf_errors[error]) + "\t" + error)
    

