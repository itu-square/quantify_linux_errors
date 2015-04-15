%title: A Quantitative Analysis of Linux Kernel
%author: Elvis Flesborg
%date: today > 1st Sep 2015

-> About Me and the Project <-
=========


o Master Thesis on ITU Copenhagen

o Claus Brabrand as supervisor

o Jean as co-supervisor


o Can we make a representative sample of all configs in Linux?

o Can we then say something statistically about this?

----------------------

-> About the Linux Kernel <-
=========

- Approximately 10,000 features.
    - 2^10,000 possible configurations.
      
    - Don\`t bother counting...


- Want to create a representative subset of all possible configurations.
  
- Say something statistically about bugs in all of Linux.
    - What types of bugs.
    - The location of the bugs.

-----------------------

-> Compiling a Linux Kernel <-
==========

- Create the configuration.
    - defconfig
    - allyesconfig
    - allnoconfig
    - tinyconfig
      
    - *_randconfig_*
      
- From that configuration compile Linux.
- Compile with \`gcc -Wall\` 
    - (Well actually the command is \`make\`)
- Collect stderr and stdout.

-----------------------

-> Creating a Representative subset <-
=========

- So GNU Make has \`make randconfig` which is random.
  But not that random...
  
- For every feature:
    - Flip a coin,
    - Starting from the top of the Kconfig file.
      
    - A parent node will have a 50-50 chance.
    - What about children?
      
    - If the two subtrees are not equal in size?
        - Number of configurations is skewed.
        - It should not have been 50-50.

-----------------------

-> Kconfig Permutations <-
=========

- Kconfig has tree-like structure.
    - Kconfig files are spread all over.
    - Concatenate the Kconfig files.
    - Flatten the structure.
    - Without losing information.
    - Permute Kconfig file.
      
    - This should be even more random... Maybe.
      (depending on how well written Kconfig is)

----------------------

-> Kconfig Transformation <-
=========

    1 if FOO
    2   config FOOBAR
    3     bool 
    4   config FOOFOO
    5     bool
    6 endif

will become

    1 config FOOBAR
    2   bool
    3   depends on FOO
    4 config FOOFOO
    5   bool
    6   depends on FOO

----------------

-> Kconfig <- 
=========

- \`depends on FOO\`
    - Will only enable feature if FOO is enabled
      
- \`select BAR\`
        - Will force BAR to be enabled.
        - Will NOT check BAR\'s dependencies. (Danger\!)
          
        - Hence the \`HAVE_BAR\` features.
          

-----------------------

-> Without HAVE_BAR <-
=========

    1 config FOO
    2   bool
    3   select BAR
    4 config BAR
    5   bool
    6   depends on FOOBAR

If Foobar is not set, we will not have a valid configuration.

-----------------------

-> HAVE_BAR <-
==========

    1 config FOO
    2   bool
    3   select HAVE_BAR
    4 config HAVE_BAR 
    5   bool
    6 config BAR
    7   bool
    8   depends on FOOBAR && HAVE_BAR

Notice HAVE_BAR has no dependencies.

-----------------------

-> Run This a Gazillion Times <-
=========

- Takes anything from 1 to 60 minutes to compile
    - tinyconfig vs. allyesconfig
      
- On a 4 core 2.5GHz (only randconfigs)
    - 2 to 30 minutes
    - Average of 8 minutes
      
- Let\`s collect 1 million
    - 8 min \* 1,000,000 / 60 min / 24 hours
    - 5555 days \!
    - 45 computers in 3 months.

-----------------------

-> Collected Information <-
=========

- Program name (linux-3.19)
- Configuration file
- Configuration errors (There sometimes are some)

- CPU
- RAM
- Time to compile
- exit status of \`make\`

- gcc version
- gcc stderr
- gcc stdout

-----------------------

-> gcc -Wall <-
=========

- uninitialized variable

# Notes
# Tell about I had 3 different ways of permuting.
#   - rewrite randconfig
#   - intercept AST
#   - permute Kconfig
#   ^ Or something like it. Look in my notebook, I don`t remember

--------------------------

-> More <-
=========

- collisions in configuration files (md5sum)
- statistics on a tree structure
