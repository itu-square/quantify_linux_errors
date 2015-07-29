Kconfig
=======

Table of contents
=================
### Grammar and syntax
## EBNF (freestyle)
## BNF (inspired by [2](Lua))
#### Rewriting the concatenated Kconfig file
### IF clauses
### Menu clauses
### DEPENDENCY TREE
### Interesting files and functions
### KconfigLib
### Optimization and making it go quicker
### References





### Grammar and syntax

The Context-free grammar for Kconfig can be read in the file:
`<kernel source>/Documentation/kbuild/kconfig-language.txt`

I have translated this to the *Extended Backus-Naur Form* (EBNF)[1]
(tried to translate)

## EBNF (freestyle)

~~~
entity      = 'config' | 'if' | 'menu' | 'mainmenu'
types       = 'int' | 'tristate' | 'bool' | 'boolean' | 'def_bool' | 'def_tristate'
              | 'string' | 'hex' ;
options     = 'modules'

uppercases  = 'A-Z' ;
numbers     = '0-9' ;
lowercases  = 'a-z' ;
characters  = uppercases | lowercases | numbers | '\_' ;

id          = uppercases | numbers, { characters } ;

statement   = entity, whitespace, id ;
~~~


## BNF (inspired by [2](Lua))

~~~
stat ::= 'config ' id '\n' options

id ::= characters { characters }

characters ::= [A-Za-z_0-9]\*

options ::= mandatory optional

types ::= 'bool' | 'boolean' | 'tristate' | 'int' | 'string' | 'hex'
deftypes ::= ( 'def_bool' | 'def_tristate' ) expr

mandatory ::= types [ '"' characters '"' ] [ expr ] |

optional ::= 'depends on ' expr
             'select ' expr
             'help\n' characters

expr ::= id [ '=' characters ] 
         expr '&&' expr |
         expr '||' expr |
         '(' expr ')'
         'if ' expr
         'menu' text
         'y'
         'n'

text ::= characters | symbols 
         text text

symbols ::= '/-(),.'
~~~


Rewriting the concatenated Kconfig file
---------------------------------------

### IF clauses

As an example, I will have an if clause like this:

~~~
if FOO
    config FOOBAR
    config BARBAR
endif
~~~

This should be rewritten to:

~~~
config FOOBAR
    depends on FOO
config BARBAR
    depends on FOO
~~~

and these config statements can thus now be randomized without the loss of 
dependencies. A more advanced form of if clause could be:

~~~
if FOO && BAR
    config FOOBAR
    config BARBAR
endif
~~~

But the expression FOO && BAR will simply be put into the depends on clause like
so:

~~~
config FOOBAR
    depends on FOO && BAR
config BARBAR
    depends on FOO && BAR
~~~
    
### Menu clauses

An example of a menu clause is as follows:

~~~
menu "Some menu title"
    config FOO
        options ...

    config BAR
        options ...
endmenu
~~~

This will not really mean anything when running `make randconfig`, since it has
no graphical interface, and thus the menus are meaningless. A rewrite could then
be like so:

~~~
config FOO
    options ...
config BAR
    options ...
~~~

The `menu` and `endmenu` parts have just been stripped away, making the
features available to randomize. It is first when the menu has dependencies, 
that we must always append these to the configs in the menu clause. 
Take this example:

~~~
menu "Some menu title"
depends on FOO
    config FOOBAR
        options ...

    config BARBAR
        options ...
endmenu
~~~

The dependency FOO will now have to be added to all of the inner features.
Just like with the if clause, the rewritten Kconfig could look like this:

~~~
config FOOBAR
    depends on FOO
    options ...

config BARBAR
    depends on FOO
    options ...
~~~

This is also clearly stated in the article [6], so maybe reference to them, 
and not write so much about this. They also say something about the `menuconfig`
expression.

### DEPENDENCY TREE

When creating the dependency tree, some features can have a variable, that look 
like this: `FOO && BAR`. This is basically the same as `FOO` and `BAR`. So as 
long as it is on 'and's it could just be one long list. Example:

~~~
config FOO
    depends on BAR && FOOBAR
    depends on BARBAR
    depends on BARFOO && FOOFOO
~~~

could be rewritten to 

~~~
config FOO
    depends on BAR && FOOBAR && BARBAR && BARFOO && FOOFOO
~~~

or

~~~
config FOO
    depends on BAR
    depends on FOOBAR
    depends on BARBAR
    depends on BARFOO
    depends on FOOFOO
~~~

But when we have 'or's in the game, they will have to be kept intact. So no 
concatenating into one big list. We will have to have a list of all the 'or's.
So the data structure for a feature's dependencies should contain two lists.
One list with the 'and's and one list with the 'or'-expressions.

### Interesting files and functions

I have extracted all the function names in both files. They are in this folder
in the files `confdata.c.functions` and `conf.c.functions`.

<src>/scripts/kconfig/confdata.c
  - 

<src>/scripts/kconfig/conf.c
  -
### KconfigLib

## Example: Count the number of features

It is important to use python2, or else it no work.

>>> import kconfiglib
>>> featuremodel = kconfiglib.Conf("../linux-3.19/Kconfig_concat", "../linux-3.19")
>>> count = 0 
>>> for features in featuremodel:
...     count += 1
...
>>> print count 
10334


### Optimization and making it go quicker

I found out today, that running `make randconfig` is much slower than running
`./script/kconfig/conf --randconfig Kconfig`.
100conf/113sec   `make randconfig`
100conf/  6sec   `./script/kconfig/conf --randconfig Kconfig`

so approximately 18 times faster.

### References

[1] https://en.wikipedia.org/wiki/Extended_Backus–Naur_Form
    Wikipedia page about the EBNF

[2] http://www.lua.org/manual/5.1/manual.html
    The Lua programming language, which has - at the bottom - the syntax written
    in BNF (not EBNF)

[3] https://eurosys2011.wordpress.com/
    something about kconfig

[4] http://www.linuxjournal.com/article/6568?page=0,1
    Very old article about Kconfig

[5] https://docs.python.org/3/reference/grammar.html
    The full Python programming language grammar.

[6] Kconfig semantics by T. Berger
    

[7] https://dl.dropboxusercontent.com/u/10406197/kconfiglib.html
    Python documentation for Kconfiglib python parser
    Really nice documentation

[8] https://en.wikipedia.org/wiki/Feature_model
    There's a little image depicting a small feature model with dependencies

[9] http://www.spinics.net/lists/linux-kbuild/
    A mailing list about kbuild

[A] http://freetz.org/browser/trunk/tools/developer/create-kconfig-warnings
    Somebody's script which creates 1000s of randconfigs?

[B] http://www.linuxjournal.com/content/kbuild-linux-kernel-build-system
    2012 article about Kbuild

