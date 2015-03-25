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
configs = []


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
        line = line.replace("\t", "    ") # Removing all tabs from the Kconfigs. They mess up my regex.
        lines.append(line)
        

concatenate(dir + "/Kconfig")


tree = {}
tree["configs"] = []

def add_layer(tree, location, lines):
    print(len(location))
    print(location)
    tree[lines[0]]["prefix"] = lines
    pass


def rm_layer(tree, location, line):
    pass


def add_config(tree, location, lines):
    
    pass
    


def create_tree(tree, lines):
    config = []
    prefix = [] # Can be multiple lines. eg. menu [..] \n depends [..]
    suffix = "" # Can only be contents of rm_layer_words
    location = [] # The path as a stack, so use pop()

    add_layer_words = ["if", "menu", "choice"]
    rm_layer_words = ["endif", "endmenu", "endchoice"]
    config_words = ["config", "menuconfig"]

    mode = "config"

    for line in lines:
        firstword = line.split(' ', 1)[0]

        if firstword in add_layer_words + rm_layer_words + config_words:
            if not config == []:
                add_config(tree, location, config)
            if not prefix == []:
                add_layer(tree, location, prefix)
            if not suffix == []:
                rm_layer(tree, location, suffix)

            config = []
            prefix = []
            suffix = ""

        if firstword in add_layer_words:
            location.append(line)
            mode = "add_layer"
        elif firstword in config_words:
            mode = "config"
        elif firstword in rm_layer_words:
            location.pop()
            mode = "rm_layer"


        if mode == "config":
            config.append(line)

        if mode == "add_layer":
            prefix.append(line)


        if mode == "rm_layer":
            suffix = line

        #print(mode + " " +  line)
        #print(location)


create_tree(tree, lines)

def print_all():
    for i in tree:
        print(i)
        for j in tree[i]:
            print("   " + str(j))

#print_all()

#segments = permutate(kconfs[5])
#print_permutation(segments)

#random.shuffle(segments)
#print_permutation(segments)





