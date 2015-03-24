# Quantifying Errors in Linux Kernel
Elvis' master thesis

## Programs and versions
`$ wget https://www.kernel.org/pub/linux/kernel/v3.x/linux-3.19.tar.xz`  
`$ wget https://www.kernel.org/pub/linux/kernel/v4.x/testing/linux-4.0-rc1.tar.xz`  
`$ wget http://www.busybox.net/downloads/busybox-1.23.1.tar.bz2`  

## Dependencies
  * python3 (maybe older versions will work)
  * bash (installed on almost all distributions)
  * gcc-multilib (or build-tools, or whatever it is called in your distribution)
      - IMPORTANT - I got some compile errors, where it stated, that I needed
        `lgcc`. The interweb told me, I should have used `gcc-multilib` in-
        stead of `gcc`. So I have now changed it to `gcc-multilib`
  * GNU time (not built-in bash-time or zsh-time, but GNU time)
  * `lzop` - I got some compilation errors stating that I needed `lzop` (It is
    a kind of compression format (think zip-zop))

I will probably create a virtual machine with all the dependencies resolved, and
post a link here, for everyone to download. But it is not ready yet.

In Arch:  
`# pacman -Syu --needed base-devel`  
`# pacman -Syu python time gcc-multilib lzop`  

## Scripts

### make_and_get_errors.sh [tarball]
This script will untar, and compile a tarbal.  

saves following files:
  * config      (the configuration, k)
  * analyzer    (which analyzer program did the errorcheck)
  * buginfo     (the results from the analyzer)
  * time        (a result of running GNU time)

### categorize_errors.py
This is a python script, because I had no idea how to use sets, and arrays in
Bash. I have made the script for Python 3.x but it is possible it will work for
earlier versions as well.
This script looks through a specific `buginfo` file, and scrapes all the info
into an aggregate, which can easilier be read.

### generate_randconfigs.sh
This script only generates the configurations. It does not compile the whole 
thing. This is handy for getting large amounts of random configurations.

### check_randconfigs.sh
I have tried to make a script, that checks how random `make randconfig` has
been. It prints the ratio of ENABLED/DISABLED/MODULE/NOT_SET of some feature
that you specify in the bottom of this file.

## Timing of the compiling process
GNU time is used in stead of the normal built-in time command. This is mainly 
to make it easier to get the time into a specific file, and in the format we 
want.



