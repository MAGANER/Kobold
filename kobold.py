#Kobold is meta-language used to improve the view of source code
#or even to create completely new language based on another one!
#exampe of use:$python kobold.py source1.cpp source2.cpp header1.h macro.ko
#syntax of Kobold is pretty simple
#macro = expr
#macro_n = expr
import sys
from functools import reduce

def get_files():
    return sys.argv[1:]
def separate(files):
    macro_file = ""
    sources    = []
    for f in files:
        if ".ko" in f and len(macro_file) == 0:
            macro_file = f
        elif ".ko" in f:
            print(f"can not get more than 1 macro file {f} is not allowed!")
            exit(-1)
            
        if ".ko" not in f:
            sources.append(f)

    return (macro_file,sources)
def read(macro_file):
    lines = []
    with open(macro_file) as f:
        for l in f:
            lines.append(l)
    return lines
def parse(lines):
    macro_table = {}
    for l in lines:
        value = l.split('->')
        if len(value) > 2:
            _value = [value[0]] 
            _value.append(reduce(lambda x,y: x+y,valuef[1:]))
            _value[1] = _value[1][:-1] #delete last \n symbol
            macro_table[_value[0]] = _value[1]
        else:
            value[1] = value[1][:-1]
            macro_table[value[0]] = value[1]
    return macro_table


def match_macros(macro_table,line):
    for key in macro_table:
        if key in line:
            new_line = line.replace(key,macro_table[key])
            return new_line
            
def match_macroses(file_path,macro_table):
    lines = []
    with open(file_path,"r") as f:
        for line in f:
            matched = match_macros(macro_table,line)
            if matched == None:
                lines.append(line)
            else:
                lines.append(matched)

    print(lines)
    with open(file_path,"w") as f:
        f.seek(0)
        f.truncate()

        for line in lines:
            f.write(line)
        


files = separate(get_files())
macro_file = files[0]
files_to_change = files[1]
macro_table= parse(read(macro_file))

for file in files_to_change:
    match_macroses(file,macro_table)
