9 april 2015
============

Next time
---------
Look into the HAVE_FOO_BAR features.
  * The HAVE_FOO features are there to relax the `select` option. This option
    does not consider dependencies of the symbol. It simply puts its value to
    [=y]. 
    All the HAVE_FOO features do not have any dependencies (well acutally they
    do), and therefore if a HAVE_FOO feature is selected, there will be no dep-
    endency issues.
    The feature FOO then depends on HAVE_FOO. FOO will never be selected, only 
    HAVE_FOO. See [2]:355.
    

Look into the choice options. how to un-clause them

look into the "target <> not remade because of errors" error just to understand what it means.

Take an error from a configuration with no configuration errors.
    And go into depth with it.
    and find the place in the code and make sure, that it is indeed uninitialized.
    (or what error it was)
    make a "simplified bug" so we can see when it is defined, initialized, and  so on
        and check with the configuration and the ifdefs.
        Just like in the vbdb.itu.dk
  * Look at [1](GNU Make) to see the error messages, that GNU make can create.
  * Also look at [3](vbdb) to see what bugs exist

Make sure that I can recreate a bug from a .config file.
  * And make sure that I reccreate everything.
      - What is not the same
      - Is more than the .config file needed to recreate everything.
  * And write down how I do it.

Try to invoke the `make -S` flag or something. So it stops everytime it
encounters just 1 error

### Error in randconfig, or just something I have to work around.

I found out that `make randconfig` will not consider configs like this:

~~~
config FOO
    bool
~~~

It will have to have some description after the type to consider the 
feature:

~~~
config FOO
    bool "Description"
~~~

Lots of features have just `bool` or `tristate` without description. I will
put in some dummy text, just to work around it.

OR maybe it is done on purpose. Maybe some of the are those HAVE_FOO_BAR configs
that should only be activated by a `select` or something.


QUESTIONS FOR NEXT MEETING
==========================
  * Consider running `make V=1` and get all that info maybe it will be useful.
  * Also consider running `make -d`
    
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

REFERENCES
==========

[1] https://www.gnu.org/software/make/manual/html_node/Error-Messages.html
    GNU Make error messages

[2] <kernel source>/Documentation/kbuild/kbuild-language.txt
    
[3] http://vbdb.itu.dk/#search/
