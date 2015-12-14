# createMakefile

An easy way to setup a Makefile for C and C++ projects. The script is compatible with Epitech's norm.

It spits out the Makefile on the standard output. You may redirect it to a Makefile using `./createMakefile [options] > Makefile` on the shell.

## How to use it

### Synopsis

Invoke the script with at least the `-S` option and valid source files, and a name (i.e. one of the following options : `-N`, `-A`, `-D`).

    ./createMakefile -S src -I include -N a.out

### Getting help

`./createMakefile --help` to get a full list of options :

    usage: createMakefile.py [-h] [-I INCLUDE] [-S SOURCE] [-N NAME] [-A ANAME]
                             [-D DNAME] [-C C++FLAGS] [-c CFLAGS] [-f FLAGS]
                             [-L LDFLAGS] [-d DEPENDENCY] [-e EXCLUDE] [--version]

    Autogenerate a Makefile

    optional arguments:
      -h, --help            show this help message and exit
      -I INCLUDE, --include INCLUDE
                            Add include directory
      -S SOURCE, --source SOURCE
                            Add source directory
      -N NAME, --name NAME  Set executable name
      -A ANAME, --aname ANAME
                            Set static library name
      -D DNAME, --dname DNAME
                            Set dynamic library name
      -C C++FLAGS, --c++flags C++FLAGS
                            Add C++ flags
      -c CFLAGS, --cflags CFLAGS
                            Add C flags
      -f FLAGS, --flags FLAGS
                            Add C and C++ flags
      -L LDFLAGS, --ldflags LDFLAGS
                            Add ld flags
      -d DEPENDENCY, --dependency DEPENDENCY
                            Add library as dependency, with directory to call make
                            in
      -e EXCLUDE, --exclude EXCLUDE
                            Exclude files matching regex
      --version             show program's version number and exit

## Features

* Creating compilation rules for `.c` and `.cpp` files.
* Source files have correct include dependancies (searched recursively in header files).
* Add a library as a dependance (will call all/clean/fclean/re when appropriate).

## Remarks and improvement

Feel free to report anything you think useful to florian.sabourin@epitech.eu.
