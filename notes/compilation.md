# Compilation 

To compile the Linux Kernel, a compiler is needed. The GNU Compiler Collection
(see [3]) is the standard compiler to use. Others can be used, but this report
will not go in depth with those. 

## Version of gcc

Jesper said, that lots had happened lately at the gcc. It had gotten better at 
finding certain bugs, or something.
I was running 4.9.2 until recently, but there is a 5.1 out from april 2015, so 
I will try to upgrade, and see.

on archlinux, I had to enable the testing, and testing-multilib repos in the
/etc/pacman.conf file. Then just `pacman -Syu`, and gcc upgraded to the newest
version 5.1 instead of 4.9.2.

install version from core with command:
`sudo pacman -S core/gcc`
This will install version 4.9.2 and replace version 5.0.1 from the multilib


## Configuration 

When compiling the Linux Kernel, the first step is to make the configuration.
This is achieved by issuing the command:

`$ make defconfig`

The `make` command looks in a file called `Makefile` or `makefile`. These
makefiles contain a list of commands that are run. Among other things lots of 
`gcc ...` commands.

If a random configuration is desirable, one can issue the command:

`$ make randconfig`

## Compiling with the configuration

After the configuration has been created, the program is compiled by simply 
issuing the command:

`$ make`

This can take everything from 3 minutes up to ~1 hour, depending on the config
and the specifications of the host machine.

However with the standard `gcc` compiler, not all possible configurations can be
succesfully compiled. If the host machine has an x86_64 architecture, for 
example, only Linux kernels with an architecture of x86_64 and i386 can be 
created. Unless a cross-compiler is used, but that is more tricky.

## Overriding the flags for  gcc

If `make -e` is run, then it will take the environment variables over the
variables that are put in the Makefiles. So for example this Makefile line:
    `HOSTCFLAGS  = -Wall -Wmissing-prototypes -Wstrict-prototypes -O2 ...`
will turn on all kinds of erros, but if I am only interested in let's say:
    `-Wuninitialized -Wmaybe-uninitialized ...` 
then I can create an environment
variable:
    `export HOSTCFLAGS="-Wuninitialized"` 
and I will only get those errors. This 
can help scale the output files down, so I only get the output that I want.

(But I can also just do that afterwards)


# Cross-compilers

To find out what architecture a machine is running, type in:

`$ gcc -dumpmachine`

Also really check out [5] and afterwards check out [4]. It is some list of 
what arguments to give when corsscompiling for the different archs.

Check out [7](github:linux-build-test) to see if I can use that script to auto-
compile for all architectures somehow.


## References

[1] https://wiki.archlinux.org/index.php/Kernels/Compilation/Traditional
    What ArchWiki has to say about compiling the Linux Kernel.
    see the comment about `make mrproper`

[2] http://preshing.com/20141119/how-to-build-a-gcc-cross-compiler/
    Tutorial on how to create a crosscompiler.

[3] https://gcc.gnu.org/

[4] https://www.kernel.org/pub/tools/crosstool/
    What the kernel has to say about crosscompilers

[5] http://www.linux.org/threads/the-linux-kernel-compiling-and-installing.5208/
    Tutorial guy giving some guidance on crosscompiling

[6] https://gcc.gnu.org/onlinedocs/gcc-4.9.2/gcc/Warning-Options.html#Warning-Options
    Good description of all the different warning/error flags.

[7] https://github.com/groeck/linux-build-test
    Someone created a script that crosscompiles for all archs. 
