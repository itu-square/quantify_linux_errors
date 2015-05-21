import sys, os, random, string


# Configuration (of this script. Not the program)
dir = sys.argv[1]
lines = []
files = []
configs = []
arch = sys.argv[2] 


        
# This goes deep into the kernel directory and concatenates all the Kconfig
# files to one big list.

## This will take all Kconfig files and concatenate to one large list
## called *lines*
def concatenate(file):
    files.append(file)
    for line in open(file):
        tmpline = line.replace("$SRCARCH", arch)
        tmpline = tmpline.replace("\"", "")
        tmpline = tmpline.replace("\n", "")
        if tmpline[:7] == "source ":
            file_to_add = dir + "/" + tmpline.strip()[7:]
            #print(file_to_add)
            concatenate(file_to_add)
            continue

        # Removing all tabs from the Kconfigs. They mess up my regex.
        # NOTE: This seems to mess up `make xxxconfig` a bit, because
        #       the *help* text is not in the same indention level... 
        line = line.replace("\t", "    ") 

        line = line.replace("\n", "")
        lines.append(line)
        

def scrap(list):
    output_list = []
    conf_words = ['config', 'menuconfig']

    for line in list:
        words = line.strip().split()
        if not len(words):
            continue
        if words[0] in conf_words:
            output_list.append("CONFIG_" + words[1])
    return output_list



concatenate(dir + "/Kconfig")
lines = scrap(lines)

for line in lines:
    print(line)
