
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
ap.add_argument("src", nargs="+", type=str, help="Source file or directory")
ap.add_argument("targ", type=str, help="Target directory for the sources")
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

sources = args.src
target = args.targ
total_file_count = 0
processed_file_count = 0


def file_to_file(src:str, targ:str):
    if args.force:
        remove(targ)
        link(src, targ)
        processed_file_count += 1
    else:
        print(f"WARNING: File {basename(src)} already exists in {dirname(targ)}")


def file_to_dir(src:str, targ:str):
    link(src, f"{targ}/{basename(src)}")
    processed_file_count += 1


def file_to_any(src:str, targ:str):
    if isfile(targ):
        file_to_file(src, targ)
    elif isdir(targ):
        file_to_dir(src, targ)
    else:
        print("Unknown type of <targ> found.")
        exit(-1)
        
def action_report(content:str):
    if args.verbose:
        print("-> " + content)
    if args.show_progress:
        width = int(0.5*os.get_terminal_size().columns)
        cursor = int(width*processed_file_count/total_file_count)
        print(
            "*" * cursor \
            + \
            " " * (width-cursor) \
            + \
            f"({processed_file_count}/{total_file_count})"
        )
        



# TODO: 需要实现正则表达式匹配
# TODO: 需要实现有颜色输出


if len(sources) == 1: 
    # special cases when there is 1 src and 1 targ 
    # and is d2f, f2f and f2d 
    source = sources[0]
    if exists(target):
        if isfile(target):
            if isfile(source):
                file_to_file(source, target)
                action_report(f"(1/1) {source} linked")
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
        action_report(f"(1/1) {source} linked")
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


if args.verbose or args.show_progress:
    for source in sources:
        if isfile(source):
            total_file_count += 1
        elif isdir(source):
            for i,j, files in os.walk(source):
                total_file_count += len(files)
        else:
            ...


for source in sources:
    if isfile(source):
        file_to_dir(source, target)
        action_report(f"({processed_file_count}/{total_file_count}) {src} linked")
    elif isdir(source):
        entries = list(os.walk(source))
        root = entries[0][0].replace(basename(entries[0][0]), "")
        # root = src path without the last level 
        # branch = last level in src path 
        # leaf = files in src sub dir
        # root + branch = path 
        ## e.g. in ../../saved/src_dir  and ../../saved/src_dir/sub_dir
        ## root = "../../saved/"
        ## branch = "src_dir" and "src_dir/sub_dir"
        for path, dirs, files in entries:
            branch = path.replace(root, "")
            os.makedirs(os.join(target, branch))
            for leaf in files:
                file_to_dir(
                    os.path.join(path, leaf), os.path.join(target, branch)
                )
                action_report(f"({processed_file_count}/{total_file_count}) {os.path.join(path, leaf)} linked")
                    
            
            
            
            
    


