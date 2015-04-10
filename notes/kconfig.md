Kconfig
-------

### Grammar and syntax

The Context-free grammar for Kconfig can be read in the file:
`kernel/Documentation/kbuild/kconfig-language.txt`

I have translated this to the *Extended Backus-Naur Form* (EBNF)[1]

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
