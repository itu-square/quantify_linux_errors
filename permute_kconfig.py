import sys, os, random, string


# Configuration (of this script. Not the program)
dir = sys.argv[1]
lines = []
files = []
configs = []


        
class Layer:
    def __init__(self, name, parent):
        self.name = name
        self.configs = []
        self.layers = []
        self.prefix = []
        self.suffix = ""
        self.parent = parent

    
    def __repr__(self):
        output = []
        for layer in self.layers:
            output.append(layer.name)
        return str(output)


    def get_name(self):
        return self.name


    def get_parent(self):
        return self.parent


    def add_configs(self, configs):
        self.configs = configs


    def add_layer(self, layer):
        self.layers.append(layer)


    def add_suffix(self, suffix):
        self.suffix = suffix

        
    def add_prefix(self, prefix):
        self.prefix.append(prefix)



# This goes deep into the kernel directory and concatenates all the Kconfig
# files to one big list.
# NOTE: the architecture must be specified. Right now "x86" is hardcoded.
# But this can be changed. But I will have to look into cross-compiling, 
# before it can be anything other than "x86" or "i386"

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

        # Removing all tabs from the Kconfigs. They mess up my regex.
        line = line.replace("\t", "    ") 

        line = line.replace("\n", "")
        lines.append(line)
        


def create_tree(lines):
    config = []
    prefix = [] # Can be multiple lines. eg. menu [..] \n depends [..]
    suffix = "" # Can only be contents of rm_layer_words
    root_layer = Layer("root", None) # The current layer name
    current_layer = root_layer

    add_layer_words = ["if", "menu", "choice"]
    rm_layer_words = ["endif", "endmenu", "endchoice"]
    config_words = ["config", "menuconfig"]

    mode = "config"


    for key, line in enumerate(lines):
        firstword = line.split(' ', 1)[0]

        if firstword in rm_layer_words:
            suffix = line
            mode = "suffix"
        if firstword in add_layer_words:
            mode = "prefix"
        if firstword in config_words:
            mode = "config"


        if firstword in add_layer_words + rm_layer_words + config_words:
            #print(str(current_layer.get_name))
            if not config == []:
                #print("new config" + str(config))
                current_layer.add_configs(config)
            if not prefix == []:
                #print(str(key)+prefix[0])
                current_layer.add_prefix(prefix)
                new_layer = Layer(str(key)+prefix[0], current_layer)
                current_layer.add_layer(new_layer)
                current_layer = new_layer
            if not suffix == "":
                #print(suffix)
                current_layer.add_suffix(suffix)
                current_layer = current_layer.get_parent()
                

            config = []
            prefix = []
            suffix = ""


        if mode == "config":
            config.append(line)

        if mode == "prefix":
            prefix.append(line)



        #print(mode + " " +  line)
    return root_layer


concatenate(dir + "/Kconfig")
tree = create_tree(lines)
print(tree)
