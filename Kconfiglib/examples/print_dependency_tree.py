# Prints a tree of all items in the configuration

import kconfiglib
import sys

def print_with_indent(s, indent):
    print (" " * indent) + s

def print_items(items, indent):
    for item in items:
        if item.is_symbol():
            #print_with_indent("config {0}".format(item.get_name()), indent)
            print(item.get_name())
            for dep in item._get_dependent():
                print("   " + dep.get_name())

conf = kconfiglib.Config(sys.argv[1], sys.argv[2])
print_items(conf.get_top_level_items(), 0)
