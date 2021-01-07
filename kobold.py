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
    if len(macro_file) == 0:
        print("you should pass macro file!")
        exit(-1)

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
        value[0] = value[0].replace(' ','')
        if len(value) > 2:
            _value = [value[0]]
            _value.append(reduce(lambda x,y: x+y,valuef[1:]))
            _value[1] = _value[1][:-1] #delete last \n symbol
            macro_table[_value[0]] = _value[1]
        else:
            value[1] = value[1][:-1]
            macro_table[value[0]] = value[1]
    return macro_table

def find_all(symbol, line):
    counter   = 0
    positions = []
    for ch in line:
        if symbol == ch:
            positions.append(counter)
        counter+= 1
    return positions

def compute_generative_expression(line,macro_table):
    result  = line
    positions = find_all('{',line)
    if len(positions) > 0:
        for pos in positions:
            end_pos = line.find("}",pos)
            if(end_pos != -1):
                sub_line = line[pos+1:end_pos]
                values = sub_line.split(',')
                if not values[0].isdigit():
                    print(f"first arg of generative expresion must be digit value! {line}")
                else:
                    new_line = int(values[0])*values[1]
                    result = result.replace(result[pos:end_pos+1],new_line)
            else:
                print(f"incorrect generative expression {line}")
        return result
    else:
        return None

def match_macros(macro_table,line):
    for key in macro_table:
        if key in line:
            computed = compute_generative_expression(macro_table[key],macro_table)
            val_to_set = ""
            if computed != None:
                val_to_set = computed
            else:
                val_to_set = macro_table[key]
            new_line = line.replace(key,val_to_set)
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
