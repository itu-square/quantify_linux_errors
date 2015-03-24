import sys, os, random


# Configuration (of this script. Not the program)
dir = sys.argv[1]
kconfs = []
oneline_delimiters = ["config", "menu"

for root, dirs, files in os.walk(dir):
    for file in files:
        if file[:7] == "Kconfig":
            kconfs.append(root + "/" + file)


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


segments = permutate(kconfs[5])
print_permutation(segments)

random.shuffle(segments)
print_permutation(segments)





