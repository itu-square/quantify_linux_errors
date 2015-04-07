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
              | 'string' ;
options     = 'modules'

uppercases  = 'A-Z' ;
numbers     = '0-9' ;
lowercases  = 'a-z' ;
characters  = uppercases | lowercases | numbers | '\_' ;

id          = uppercases | numbers, { characters } ;

statement   = entity, whitespace, id ;
~~~


## BNF (inspired by [2])

~~~
stat ::= 'config ' id '\n' options

id ::= characters { characters }

characters ::= [A-Za-z_0-9]

options ::= mandatory optional

types ::= 'bool' | 'boolean' | 'tristate'
deftypes ::= 'def_bool' | 'def_tristate' 

mandatory ::= types [ '"' characters '"' ] [ expr ] |

clause ::= 'if' expr

expr ::= id [ '=' characters ] 
         expr '&&' expr |
         expr '||' expr |
         '(' expr ')'

text ::= characters | symbols 

symbols ::= '/-(),.'
~~~



### References

[1] https://en.wikipedia.org/wiki/Extended_Backus–Naur_Form
    Wikipedia page about the EBNF

[2] http://www.lua.org/manual/5.1/manual.html
    The Lua programming language, which has - at the bottom - the syntax written
    in BNF (not EBNF)



