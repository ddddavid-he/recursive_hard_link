
"""
This program provides you with a 
recursive version of hard link command `ln`
which is able to backup directories
"""

import os
import argparse 

version_ap = argparse.ArgumentParser(description="Version Argument")
version_ap.add_argument("-V", "--version", required=False, action="store_true")
show_version = version_ap.parse_args()
if show_version:
    print("Version 0.1 \nBy Ddddavid 23/10/07")
    exit(0)

ap = argparse.ArgumentParser(description="Recursive Hard Link Tool")
ap.add_argument("src", nargs="+", help="Source file or directory")
ap.add_argument("targ", help="Target directory for the sources")
ap.add_argument("-f", "--force", required=False, action="store_true",
                help="Overwrite existing files or directories")
ap.add_argument("--mirror", required=False, action="store_true",
                help="Synchronize target dir and src dir")
ap.add_argument("-v", "--verbose", required=False, action="store_true",
                help="Display detailed debugging message to console")
ap.add_argument("--show-progress", required=False, action="stroe_true",
                help="Display progress")


args = ap.parse_args()


from os.path import basename, dirname, isdir, isfile, exists
from os import makedirs, remove, removedirs, link


def file_to_file(src, targ):
    if args.force:
        remove(targ)
        link(src, targ)
        exit(0)
    else:
        raise FileExistsError(f"File {basename(src)} already exists in {dirname(targ)}")


def file_to_dir(src, targ):
    link(src, f"{targ}/{basename(src)}")


def file_to_any(src, targ):
    if isfile(targ):
        file_to_file(src, targ)
    elif isdir(targ):
        file_to_dir(src, targ)
    else:
        print("Unknown type of <targ> found.")
        exit(-1)



sources = args.src
target = args.targ

if len(sources) == 1: 
    # special cases when there is 1 src and 1 targ 
    # and is d2f, f2f and f2d 
    source = sources[0]
    if exists(target):
        if isfile(target):
            if isfile(source):
                file_to_file(source, target)
            elif isdir(source):
                raise IsADirectoryError("<src> is directory while <targ> provided as a file name")
            else:
                print("Unknown type of <targ> found.")
                exit(-1)
        elif isdir(target):
            file_to_dir(source, target)
        else:
            print("Unknown type of <targ> found.")
            exit(-1)
    else:
        # parent = dirname(target)
        # if exists(parent):
        #     if isdir(parent):
        #         file_to_file(src, f"{parent}/{basename{target}}")
        # THE ABOVE IS NOT NECESSARY. LINK WILL HANDLE THAT.
        ...
    exit(0)
    

# normal cases 
if not exists(target):
    raise FileNotFoundError(f"Dir {target} does not exists")

## if there are more than 1 files in <src> 
## or any dirs, <targ> has to be a dir.
## So, when there are more than one <src>s, 
## the <targ> has to be dir.
if not isdir(target):
    raise NotADirectoryError(f"{target} is not a directory")


for source in sources:
    if isfile(source):
        file_to_dir(source, target)
    elif isdir(source):
        for path, dirs, files in os.walk(source):
            makedirs(path)
            
            
    


