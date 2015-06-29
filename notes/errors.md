Errors in make
==============

# Date : 23 Jun 2015

These numbers are from stderrs in 850 differenct compilations.
So they may be different later on when I get more compilations done.
But for now, it may say something anyways.

‘[foo] Error NN’            
‘[foo] signal description’

    NOT make errors. Errors from a subprocess.
    if prefixed with *** then it is fatal, and will stop.

    1485 occurences
    0 occurences

‘missing separator. Stop.’
‘missing separator (did you mean TAB instead of 8 spaces?). Stop.’

    `make` did not understand the line it was reading.
    maybe there were spaces instead of tabs.

    0 occurences
    0 occurences

‘recipe commences before first target. Stop.’
‘missing rule before recipe. Stop.’

    0 occurences
    0 occurences

‘No rule to make target `xxx'.’
‘No rule to make target `xxx', needed by `yyy'.’

    0 occurences
    52 occurences

‘No targets specified and no makefile found. Stop.’
‘No targets. Stop.’

    0 occurences
    0 occurences

‘Makefile `xxx' was not found.’
‘Included makefile `xxx' was not found.’

    0 occurences
    0 occurences

‘warning: overriding recipe for target `xxx'’
‘warning: ignoring old recipe for target `xxx'’

    0 occurences
    0 occurences

‘Circular xxx <- yyy dependency dropped.’

    0 occurences

‘Recursive variable `xxx' references itself (eventually). Stop.’

    0 occurences

‘Unterminated variable reference. Stop.’

    0 occurences

‘insufficient arguments to function `xxx'. Stop.’

    0 occurences

‘missing target pattern. Stop.’
‘multiple target patterns. Stop.’
‘target pattern contains no `%'. Stop.’
‘mixed implicit and static pattern rules. Stop.’

    0 occurences
    0 occurences
    0 occurences
    0 occurences

‘warning: -jN forced in submake: disabling jobserver mode.’

    0 occurences

‘warning: jobserver unavailable: using -j1. Add `+' to parent make rule.’

    0 occurences

