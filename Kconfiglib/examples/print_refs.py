# Prints the names of all symbols that reference a particular symbol. (There's
# also a method get_selected_symbols() for determining just selection
# relations.)

import kconfiglib
import sys

conf = kconfiglib.Config(sys.argv[1], sys.argv[2])

for sym in conf:
    print sym.get_name() + " " + str(sym.get_type())
