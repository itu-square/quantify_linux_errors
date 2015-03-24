import sys, os, random, string


# Configuration (of this script. Not the program)
dir = sys.argv[1]
kconfs = []
oneline_delimiters = ["config", "menu"]

#for root, dirs, files in os.walk(dir):
    #for file in files:
        #if file[:7] == "Kconfig":
            #kconfs.append(root + "/" + file)


def permutate(file):
    segments = []
    lines = []
    for line in open(file):
        if line.strip() == "":
            segments.append(lines)
            lines = []
            continue
        lines.append(line.strip())
    segments.append(lines) # append the last segment
    return segments

def print_permutation(segments):
    for segment in segments:
        first = 1
        help = 0
        for line in segment:
            if first == 1:
                print(line)
                first = 0
            else:
                if help == 0:
                    print("    " + line)
                else:
                    print("      " + line)

            if line.strip() == "help":
                help = 1
        print()


lines = []
files = []


def concatenate(file):
    files.append(file)
    for line in open(file):
        tmpline = line.replace("$SRCARCH", "x86")
        tmpline = tmpline.replace("\"", "")
        tmpline = tmpline.replace("\n", "")
        if tmpline[:7] == "source ":
            file_to_add = dir + "/" + tmpline.strip()[7:]
            #print(file_to_add)
            concatenate(file_to_add)
            continue
        line = line.replace("\n", "")
        lines.append(line)
        

concatenate("linux-3.19/Kconfig")

def print_all():
    for line in lines:
        print(line)

configs = []
segments = []

def put_in_segments(lines):
    layer = 0
    for line in lines:
        print(layer)
        if line[:3] == "if ":
            layer += 1
        if line[:5] == "endif":
            layer -= 1
        if line[:5] == "menu ":
            layer += 1
        if line[:7] == "endmenu":
            layer -= 1

put_in_segments(lines)

#segments = permutate(kconfs[5])
#print_permutation(segments)

#random.shuffle(segments)
#print_permutation(segments)





