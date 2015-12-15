#! /usr/bin/env python2

import os
import sys
import pwd
import time
import re
import argparse

# TODO: use argparse

def recurDependanciesOf(file, incdirs, deptab):
    ifs = open(file, 'r')
    for line in ifs:
        match = re.match("^\# *include \"(.*)\"", line, re.M);
        if match:
            includefile = match.group(1)
            for dir in incdirs:
                path = os.path.join(dir, includefile)
                if path not in deptab:
                    if os.path.isfile(path):
                        deptab.append(path)
                        recurDependanciesOf(path, incdirs, deptab)
                        break
    ifs.close()
    return deptab

# Get dependancies of a file
# Parses #include directives recursively
def dependanciesOf(file, incdirs):
    deptab = []
    return recurDependanciesOf(file, incdirs, deptab)

def get_arguments():
    parser = argparse.ArgumentParser(description='Autogenerate a Makefile')
    parser.add_argument("-I", "--include", type=str, action="append", help="Add include directory", default=[])
    parser.add_argument("-S", "--source", type=str, action="append", help="Add source directory", default=[])
    parser.add_argument("-N", "--name", type=str, action="store", help="Set executable name", default="")
    parser.add_argument("-A", "--aname", type=str, action="store", help="Set static library name", default="")
    parser.add_argument("-D", "--dname", type=str, action="store", help="Set dynamic library name", default="")
    parser.add_argument("-C", "--c++flags", type=str, action="append", help="Add C++ flags", default=[])
    parser.add_argument("-c", "--cflags", type=str, action="append", help="Add C flags", default=[])
    parser.add_argument("-f", "--flags", type=str, action="append", help="Add C and C++ flags", default=[])
    parser.add_argument("-L", "--ldflags", type=str, action="append", help="Add ld flags", default=[])
    parser.add_argument("-d", "--dependency", type=str, action="append", help="Add library as dependency, with directory to call make in", default=[])
    parser.add_argument("-e", "--exclude", type=str, action="append", help="Exclude files matching regex", default=[])
    parser.add_argument('--version', action='version', version='%(prog)s 0.1 (alpha)')
    result = parser.parse_args()
    args = dict(result._get_kwargs())
    return args


# +---------------+
# | main function |
# +---------------+
def main():
    argdict = get_arguments()

    srcdirs = argdict['source']
    incdirs = argdict['include']
    exename = argdict['name']
    libname = argdict['aname']
    soname = argdict['dname']
    cflags = " ".join(argdict['flags']) + " " + " ".join(argdict['cflags']) + " "
    cxxflags = " ".join(argdict['flags']) + " " + " ".join(argdict['c++flags']) + " "
    ldflags = " ".join(argdict['ldflags']) + " "
    excludes = argdict['exclude']
    cfiles = []
    cppfiles = []

    libs = []
    ldlibrarypath = []
    for pairstr in argdict['dependency']:
        pair = pairstr.split(',')
        if len(pair) != 2:
            print "Fatal: Invalid library pair: " + pairstr
            return
        libs.append(pair)

    if len(srcdirs) == 0:
        print "Fatal: No input directory"
        return
    if exename == "" and libname == "" and soname == "":
        print "Fatal: No executable or library name"
        return

# Review c(xx)flags and ldflags
    for dir in incdirs:
        cflags += "-I" + dir + " "
        cxxflags += "-I" + dir + " "
    for libpair in libs:
        libfile = libpair[0]
        libdir = libpair[1]
        lname = os.path.basename(libfile)
        if lname.startswith('lib'):
            lname = lname[3:]
        if lname.endswith('.a'):
            lname = lname[:-2]
        ldflags = "-l" + lname + " " + ldflags
        if libdir not in ldlibrarypath:
            ldlibrarypath.append(libdir)
    for path in ldlibrarypath:
        ldflags = "-L" + path + " " + ldflags

# List source files
    for dir in srcdirs:
        for file in os.listdir(dir):
            filename = os.path.join(dir, file)
            ok = 1
            for pattern in excludes:
                if re.match(pattern, file):
                    ok = 0
                    break
            if ok == 1:
                if filename.endswith('.cpp'):
                    cppfiles.append(filename)
                elif filename.endswith('.c'):
                    cfiles.append(filename)
    if len(cfiles) + len(cppfiles) == 0:
        print "Fatal: No input files"
        return

# Print Makefile to stdout
    print "##"
    print "## Makefile for  in " + os.getcwd()
    print "##"
    print "## Made by " + pwd.getpwuid(os.getuid())[4]
    print "## Login   <" + os.environ['USER'] + "@epitech.net>"
    print "##"
    print "## Started on  " + time.strftime("%a %b %d %H:%M:%S %Y ") + pwd.getpwuid(os.getuid())[4]
    print "## Last " + "update " + time.strftime("%a %b %d %H:%M:%S %Y ") + pwd.getpwuid(os.getuid())[4]
    print "##"
    print

# Print executable shortcuts
    print "# Executables"
    print "CC		=	gcc"
    print "CXX		=	g++"
    print "AR		=	ar rcs"
    print "RM		=	@rm -vf"
    print "MAKE		+=	--no-print-directory"
    print

# Print output program/library name(s)
    nbset = 0;
    print "# Names"
    if exename != "":
        print "NAME		=	" + exename
        nbset = nbset + 1
    if libname != "":
        print "LIBNAME		=	" + libname
        nbset = nbset + 1
    if soname != "":
        print "SONAME		=       " + soname
        nbset = nbset + 1
    print

# Print flags
    print "# Flags"
    print "CFLAGS		=	" + cflags
    print "CXXFLAGS	=	" + cxxflags
    print "LDFLAGS		=	" + ldflags
    print

# Print source files
    print "# Files"
    for i in range (len(cfiles)):
        if i == 0:
            print "CSRC		=	" + cfiles[i]
        else:
            print "CSRC		+=	" + cfiles[i]
    if len(cfiles) > 0:
        print
    for i in range (len(cppfiles)):
        if i == 0:
            print "CXXSRC		=	" + cppfiles[i]
        else:
            print "CXXSRC		+=	" + cppfiles[i]
    print

# Print obj variable
    print "# Objects"
    print "OBJ		=	$(CSRC:.c=.o) $(CXXSRC:.cpp=.o)"
    print

################### RULES ###################
    print "# Rules"

# Print all rule first if there is more than one main rule
    if nbset != 1:
        allrule = "all:"
        if exename != "":
            allrule += " $(NAME)"
        if libname != "":
            allrule += " $(LIBNAME)"
        if soname != "":
            allrule += " $(SONAME)"        
        print allrule
        print

# Print $(*NAME) rules
    if exename != "":
        namedeps = ""
        for libpair in libs:
            namedeps += libpair[0] + " "
        namedeps += "$(OBJ)"
        print "$(NAME): " + namedeps
        print "	$(CXX) -o $(NAME) $(OBJ) $(LDFLAGS)"
    if libname != "":
        print "$(LIBNAME): $(OBJ)"
        print "	$(AR) $(LIBNAME) $(filter-out main.o, $(OBJ))"
    if soname != "":
        print "$(SONAME): $(OBJ)"
        print "	$(CC) -o $(SONAME) $(filter-out main.o, $(OBJ)) $(LDFLAGS) -shared"
    print

# Print library rules
    for libpair in libs:
        print libpair[0] + ":"
        print "	@$(MAKE) -C " + libpair[1]
        print

# Print all rule if there is one main rule
    if nbset == 1:
        if exename != "":
            print "all: $(NAME)"
        if libname != "":
            print "all: $(LIBNAME)"
        if soname != "":
            print "all: $(SONAME)"
        print

# Print clean rule
    print "clean:"
    print "	$(RM) $(OBJ)"
    for libpair in libs:
        print "	@$(MAKE) -C " + libpair[1] + " clean"
    print
    
# Print fclean rule
    print "fclean:"
    fcleanstr = "	$(RM) $(OBJ)"
    if exename != "":
        fcleanstr += " $(NAME)"
    if libname != "":
        fcleanstr += " $(LIBNAME)"
    if soname != "":
        fcleanstr += " $(SONAME)"
    print fcleanstr
    for libpair in libs:
        print "	@$(MAKE) -C " + libpair[1] + " fclean"
    print

# Print re rule
    print "re: fclean all"
    print

# Print .PHONY target (adding .a files so they are recompiled)
    phonystr = ".PHONY: 	all clean fclean re"
    for libpair in libs:
        phonystr += " " + libpair[0]
    print phonystr
    print

# Print each file's target
    for file in cppfiles:
        deptab = dependanciesOf(file, incdirs)
        objfile = file[:-3] + 'o'
        filedeps = file
        for dep in deptab:
            filedeps += " " + dep
        print objfile + ": " + filedeps
        print "	$(CXX) $(CXXFLAGS) -c -o " + objfile + " " + file
        print

    for file in cfiles:
        deptab = dependanciesOf(file, incdirs)
        objfile = file
        objfile = file[:-1] + 'o'
        filedeps = file
        for dep in deptab:
            filedeps += " " + dep
        print objfile + ": " + filedeps
        print "	$(CC) $(CFLAGS) -c -o " + objfile + " " + file
        print

# +--------------------+
# | Call main function |
# +--------------------+
if __name__ == "__main__":
    main()
