# Compilation 

To compile the Linux Kernel, a compiler is needed. The GNU Compiler Collection
(see [3]) is the standard compiler to use. Others can be used, but this report
will not go in depth with those. 

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


# Cross-compilers

To find out what architecture a machine is running, type in:

`$ gcc -dumpmachine`



## References

[1] https://wiki.archlinux.org/index.php/Kernels/Compilation/Traditional
    What ArchWiki has to say about compiling the Linux Kernel.
    see the comment about `make mrproper`

[2] http://preshing.com/20141119/how-to-build-a-gcc-cross-compiler/
    Tutorial on how to create a crosscompiler.

[3] https://gcc.gnu.org/
