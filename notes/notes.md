================================================================================
  x Maybe not do this
  o Thing to do
  + Thing that I MUST do
  F Figure
  ~ Done


=== TODO ===


    === Questions
      o Differentiate 'tween invalid configurations and nonsense configurations.
        In regards to: can it compile, but will it EVER be compiled by anyone.
        But I will probably not meet these since I am using randconfig, and not
        generateNfilter


    === Write about
      o Write about all the warning types.
          o Mention in the section about all bugs, that I do not talk about bugs, 
            which I did not find any of.
      F Make a laptop model insstad  of a car one.
      o That `make` always runs `gcc -Wall` (I found out that 55/2000 times it 
        does not run -Wall but only `gcc`
          o Mention that I kinda cannot control if Wall is enabled by all.
            And that sometimes (55/2000) coders do it themselves.
      o Maybe I should have put `gcc -Wextra`
      o Find out the number of HAVE_XXXs, because those are maybe not `real` 
        features.
      o mtlab.itu.dk being able to unpack it all in RAM.
      o Write the Backus Naur Form of the Kconfig syntactic language.
      o Abstract Syntax Trees and parsers (is randconfig a parser?)
      o Version of gcc, and that a lot has happened lately (Some are compiled 
        with 4.9, and others with 5.1)
          o I hope, that I have noted this down somewhere.
      o Makefiles
         Fx Maybe make a graph showing the order of commands that are needed to 
            run. `make config (makefiles)` -> `gcc` -> `make (makefiles)` -> 
            `gcc`
      o How to unclause a choice option
      F Figure of how the permutation can be. something with aggregates of 7 
        layers, and then showing either the top level scrambled, or all of them 
        scrambled.
      o I used kconfiglib, but not for much
      o Permutations didnt do squat. ( I think)
      o `randconfig` will sometimes make an invalid config (25% actually)
      o Sketch up how Jaccard similarity can be used to find the features that 
        cause a specific error.
      ~ the UM (Linux User Mode) arch
      o TTV: DERIVED and CAPABILITY features will never be chosen by `make 
        randconfig`, and lots of configurations will never be created.
      ~ Write about why I do not cross compile, and what archs I can compile for
      o Compare bugs to 42bugs paper
      o Mention that security/ has basically no errors.
      o Explain small paragraph of each warning. 
        Make the examples real (and maybe simplified)
      o Write about security/, and about how it has not really been touched.
      o pointer-to-int is normally bad, but is used in Linux to emulate OOS

      ~ Write about 100,000 generated configs, and that I will not do it, but
        mention it. Or something.

    === SQL queries ===

      o This one shows the top warnings from unstable configs with errors.

        select type, count(config) from (select distinct type, config from 
        bugs where linux_version rlike 'next' and config in (select hash from 
        configurations where exit_status = 1 and linux_version rlike 'next')) 
        as a group by type order by count(config) desc;

        You can exchange the 'next' with '4.1.1', to get stable

      o This will get all the configurations where the warning had something
        to do with SECCOMP

        select count(distinct config) from bugs where linux_version rlike 
        'next' and original rlike 'seccomp';
    




=== Host errors ===

            Next    4.1.1   
--------------------------
seccomp     2046    2471
chaoskey    146     0
quantify    18      5
nouveau     1949    2954
i2c         6387    6459

# Found with this SQL query:

    select count(distinct config) from bugs where linux_version rlike 'next' and
    original not rlike 'seccomp' and original rlike 'i2c';

Maybe look at what files are the top files.
This query will get the top files from the bugs, that have errors.

    select distinct path, count(*) from files where bug_id in (select hash 
    from bugs where linux_version rlike 'next' and type = 'makeMsg' ) group by 
    path order by count(*) desc limit 30;




    === Programming wise ===

      o Does configuration warnings have anything to say to the error percentage?
            === 4.1.1 ===
        err_pct without conf errs = 2605/15754 = 17%
        err_pct with conf errs = 1007/5276 = 19%
            === next ===
        err_pct without conf errs = 4317/12052 = 36
        err_pct with conf errs = 3594/8977 = 40%

        # 2605 :
            # select config from bugs where config in (select hash from 
                configurations where conf_errs not rlike 'warning' and 
                linux_version rlike '4.1.1') and type = 'makeMsg' and 
                linux_version rlike '4.1.1'
        # 15754
            # select hash from configurations where conf_errs not rlike 
                'warning' and linux_version rlike '4.1.1'
        

      o Look into ERRORS, and make top 10 of that.
          o Are there any wrong errors? Are there many of the same errors?

      o Top 10 warnings inside subsystems? Is this too much data?

      o How many new features are there in kconfig in linux-next compared to 
        4.1.1?

      o Look into mm/ and make a top 10 subsystem

      o Top 10 subsystemwarnings should have bugs/LOC (as a percentage)


      ~ Try to run some configs and running `mrproper` between them.
        Then run the same configs, and do not run `mrproper` in between.
        Is the warning output the same?
          # I have started this experiment. (30. july 02:00)
          # It looks as if it does not matter. But I have only run 10. Running 
            10 more

      ~ Make test configs and permute them to see that it wont do squat.

      o Does randconfig always take the default values?

      o If I run `make allnoconfig`, what are the `int` and `string` values set 
        to?

      o Is the preprocessed code stored on HDD after compilation

      x Do Jaccard similarity to find out what features cause the same errors.

      x Start a generate n filter instance to find the number of valid configs
          x Can I figure it out logically? 
          x Or start a script (that has no crossconstraints) that increases the 
            amount of features, and then checks how many are valid

      ~ Has security/ even been touched.
          ~ Not really

      ~ Backup the database

      ~ Test if randconfig does not consider features that does not have a 
        description. If it does not, all the data might be kind of bogus.
          # I have started an experiment, which creates 1000 randconfigs.
            I can use these to check if some of the *no_prompts* are enabled
            by randconfig, or only by other features that *select* them.
          # But they might just create nonsense configurations. (Also write 
            about that)
          # There ARE features that have not been enabled in 1000 randconfigs.
            It MIGHT be because there are `select CONFIG_XXX=n` somewhere.
            But there AREN'T
              $ grep "^\ *select\ .*\ " concatenated_kconfig | grep n # 9 matchs
              $ grep "^\ *select\ .*\ " concatenated_kconfig | grep m # 1 match
              $ grep "^\ *select\ .*\ " concatenated_kconfig | grep y # 5 matchs
            And all of these are lines like:
            `select FOO if BAR = n`
            THIS MEANS that they are NOT selected by `make randconfig` so the
            no-prompts are dead features, that can only be enabled by `select`s
          # Threat to validity: representativeness gets worse

      ~ Remove bogus data from database
          # View of all configurations NOT in pairs:
              > create view loners as 
              > select distinct hash 
              > from configurations 
              > group by hash 
              > having count(*) = 1;
          # All bugs from these configurations:
              > create view loners_bugs as
              > select hash from bugs
              > where config in 
              > ( select hash from loners );
          # All files from these bugs:
          # (This takes around 3-4 minutes to run)
              > create view loners_files as
              > select id,bug_id from files 
              > where bug_id in 
              > ( select hash from loners_bugs );
          # I have started to copy the database to my own computer from a file
          # Export from server:
              $ mysqldump -h mydb.itu.dk -u elvis_thesis -plinux > dump_<date>
          # Import to local machine:
              $ cat dump_<date> | mysql -u root -plinux elvis_thesis
          # Delete the bogus data:
              > delete from loners_files;
              > delete from loners_bugs;
              > delete from configurations where hash in (select * from loners);

      ~ How many ERRORS have conf_errs.?
          ~ It look like there is not a 100% correlation.
            17 % of stable have ERRORS
                28% of those have config errors
            38 % of next have ERRORS
                45% of those have config errors

=== FIND LINKS FOR THIS ===
  o TypeChef
  o kconfiglib

=== REFERENCES ===
[1] http://www.linux.org/threads/the-linux-kernel-configuring-the-kernel-part-1.4274/
    A tutorial on how to compile the kernel with info on different 
    configuration methods and such There is also a part two, that I have not 
    read.

[2] https://www.kernel.org/pub/software/scm/git/docs/user-manual.html#how-to-check-out
    A tutorial on git, which I can probably use to dig around old versions of  
    the kernel on their git site.

[3] https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html
    A long documentation on gcc. It specifies what gcc -Wall does for example.
    Which can probably come in handy at some point.

[4] http://vbdb.itu.dk/
    An online database which belongs to the paper '42 Variability Bugs In Linux'

[5] http://www3.ntu.edu.sg/home/ehchua/programming/cpp/gcc_make.html
    Something about the use of gcc and make.

[6] https://www.kernel.org/doc/Documentation/kbuild/kconfig.txt
    Something about kconfig

[7] http://www.mjmwired.net/kernel/Documentation/kbuild/kconfig.txt
    Ca. down 40% there is some notes on randconfig and what KCONFIG_SEED means.

[8] http://www.linuxquestions.org/questions/linux-hardware-18/compiling-64-bit-kernel-in-32-bit-linux-240183/
    A note on crosscompiling

[9] Gnu Make manpage
    A reference to how Gnu Make works, and the exit statuses

[A] https://code.google.com/p/distcc/
    A distributed C/C++ compiler. It may be useful. But probably not.

[B] http://www3.ntu.edu.sg/home/ehchua/programming/cpp/gcc_make.html
    About Preprocessing

[C] http://www.linuxfromscratch.org/lfs/view/stable/chapter08/kernel.html
    Howto on compiling the kernel. Do not rely on the kernel tree to be clean 
    after untarring.

[D] http://www.buildroot.org/downloads/manual/manual.html
    They have some clarifications on Kconfig language

[E] http://www.tldp.org/HOWTO/Lex-YACC-HOWTO.html
    yacc and bison explaination

[F] https://www.gnu.org/software/make/manual/html_node/Error-Messages.html
    Something about the different Error outputs in GNU make.

[G] https://wiki.archlinux.org/index.php/Kernels/Compilation/Traditional
    What ArchWiki has to say about compiling the Linux Kernel.
    see the comment about `make mrproper`

[H] http://preshing.com/20141119/how-to-build-a-gcc-cross-compiler/
    Tutorial on how to create a crosscompiler.

[I] https://gcc.gnu.org/

[J] https://www.kernel.org/pub/tools/crosstool/
    What the kernel has to say about crosscompilers

[K] http://www.linux.org/threads/the-linux-kernel-compiling-and-installing.5208/
    Tutorial guy giving some guidance on crosscompiling

[L] https://gcc.gnu.org/onlinedocs/gcc-4.9.2/gcc/Warning-Options.html#Warning-Options
    Good description of all the different warning/error flags.

[M] https://github.com/groeck/linux-build-test
    Someone created a script that crosscompiles for all archs.

[N] https://en.wikipedia.org/wiki/Extended_Backus–Naur_Form
    Wikipedia page about the EBNF

[O] http://www.lua.org/manual/5.1/manual.html
    The Lua programming language, which has - at the bottom - the syntax written
    in BNF (not EBNF)

[P] https://eurosys2011.wordpress.com/
    something about kconfig

[Q] http://www.linuxjournal.com/article/6568?page=0,1
    Very old article about Kconfig

[R] https://docs.python.org/3/reference/grammar.html
    The full Python programming language grammar.

[S] Kconfig semantics by T. Berger
        

[T] https://dl.dropboxusercontent.com/u/10406197/kconfiglib.html
    Python documentation for Kconfiglib python parser
    Really nice documentation

[U] https://en.wikipedia.org/wiki/Feature_model
    There's a little image depicting a small feature model with dependencies

[V] http://www.spinics.net/lists/linux-kbuild/
    A mailing list about kbuild

[W] http://freetz.org/browser/trunk/tools/developer/create-kconfig-warnings
    Somebody's script which creates 1000s of randconfigs?

[X] http://www.linuxjournal.com/content/kbuild-linux-kernel-build-system
    2012 article about Kbuild

[Y] http://neuling.org/linux-next-size.html

[Z] http://kisskb.ellerman.id.au/kisskb/matrix
    Some kind of build robot results page

[00]    http://git.kernel.org/cgit/linux/kernel/git/next/linux-next.git/tree/
        Next/Trees ?id=HEAD
        All the git repos that linux-next merges.
