9 april 2015
============

Next time
---------
    
__Look into the choice options. how to un-clause them__
There are two kinds of choice blocks. A one-choice, and a multiple-choice one.
multi-choice has:

    choice 
        tristate "some text"
    config FOO

one-choice has:
    choice
    config FOO
    config BAR

But so far, I have only found one multiple-choice (USB Gadget Drivers)
There will probably be some more, or the same in all the different 
architectures. (I only searched through the x86 one)

__look into the "target <> not remade because of errors" error just to understand what it means.__


__simplified bug__
Take an error from a configuration with no configuration errors.
    And go into depth with it.
    and find the place in the code and make sure, that it is indeed uninitialized.
    (or what error it was)
    make a "simplified bug" so we can see when it is defined, initialized, and  so on
        and check with the configuration and the ifdefs.
        Just like in the vbdb.itu.dk
  * Look at [1](GNU Make) to see the error messages, that GNU make can create.
  * Also look at [3](vbdb) to see what bugs exist

__make V=1 randconfig__
_Files that were interesting:_
  * scripts/kconfig/conf.c       # A bit of overview of how it is done. not rly.
  * scripts/kconfig/zconf.tab.c  # bison parser - I donnunnerstan nuttin...
  * scripts/kconfig/zconf.lex.c  # something lex lex
  * scripts/kconfig/zconf.hash.c # contains (at least) all the keywords from 
                                   the kconfig language. #

  + scripts/kconfig/confdata.c   # More on randconfig inner workings.
                                   Probability and such. (90%-bot)
                                   conf_set_all_new_symbols(...) #


__other__
Make sure that I can recreate a bug from a .config file.
  * And make sure that I reccreate everything.
      - What is not the same
      - Is more than the .config file needed to recreate everything.
  * And write down how I do it.

Try to invoke the `make -S` flag or something. So it stops everytime it
encounters just 1 error

### Error in randconfig, or just something I have to work around.

I found out that `make randconfig` will not consider configs like this:

    config FOO
        bool

It will have to have some description after the type to consider the 
feature:

    config FOO
        bool "Description"

or

    config FOO
        bool
        prompt "foo"

Lots of features have just `bool` or `tristate` without description. I should
put in some dummy text, just to work around it.

OR maybe it is done on purpose. Maybe some of the are those HAVE_FOO_BAR configs
that should only be activated by a `select` or something.

### The permutations might not be needed

It seems like it does not just flip a coin from the top. Or else it follows 
dependencies. Hmm.




QUESTIONS FOR NEXT MEETING
==========================
  * Should I remove the default values?
  * Is it really necessary to permute Kconfig?
  * How to unclause the `choice` symbol
    
DONE
====

Remember to save what architecture is being compiled for.
  - Well this is sort of saved within the .config file, so maybe not spend
    too much time on this.
    [DONE]

Look into the AST (bison and maybe yacc)
  - I have Kconfiglib.py, so I guess that is what I'm using as a parser.
    [github:ulfalizer/Kconfiglib]
    [DONE]

  * Consider running `make V=1` and get all that info maybe it will be useful.
      - Also consider running `make -d`
      - I will get waaay too much information.
      - I can do this when debugging a specific configuration afterwards.
    [DONE]

REFERENCES
==========

[1] https://www.gnu.org/software/make/manual/html_node/Error-Messages.html
    GNU Make error messages

[2] <kernel source>/Documentation/kbuild/kbuild-language.txt
    
[3] http://vbdb.itu.dk/#search/
