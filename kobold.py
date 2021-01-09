#Kobold is meta-language used to improve the view of source code
#or even to create completely new language based on another one!
#exampe of use:$python kobold.py source1.cpp source2.cpp header1.h macro.ko
#syntax of Kobold is pretty simple
#macro   = expr
#macro_n = expr
#Also there is an ability to generate expression
#macro = {n,expr} some another expression
#Instead of macro there will be expression duplicated n times

import sys
from functools import reduce

#functions to get data to process
def get_files():
    return sys.argv[1:]
def separate(files):
    '''separates terminal arguments to get sources and macro file'''
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
    '''read macro file and create hash table of macroses'''
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
#####

#special functions
def find_all(symbol, line):
    '''returns the position of any symbol contained with line'''
    counter   = 0
    positions = []
    for ch in line:
        if symbol == ch:
            positions.append(counter)
        counter+= 1
    return positions

def compute_generative_expression(line,macro_table):
    '''compute expression: {n, expr}'''
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

#main functions 
def match_macro(macro_table,line):
    '''process all macroses within the line'''
    counter = 0

    take_key = lambda counter, table: list(macro_table.keys())[counter]
    while counter < len(macro_table):
        key = take_key(counter,macro_table)
        if key in line:
            computed = compute_generative_expression(macro_table[key],macro_table)
            val_to_set = ""
            if computed != None:
                val_to_set = computed
            else:
                val_to_set = macro_table[key]
            new_line = line.replace(key,val_to_set)
            return new_line
        counter+= 1
def match_macroses(file_path,macro_table):
    '''process all files'''
    lines = []
    with open(file_path,"r") as f:
        for line in f:
            matched = match_macro(macro_table,line)
            if matched == None:
                lines.append(line)
            else:
                lines.append(matched)
    return lines

def pass_value(line,macro_table):
    new_line = []
    words = line.split(' ')
    not_changed_counter = 0
    for word in words:
        if len(word) > 0:
            check_is_macro = word[0] == r'$'
            is_macro = word[1:] in macro_table
            if check_is_macro and is_macro:
                macro_val = macro_table[word[1:]]
                computed = compute_generative_expression(macro_val,macro_table)
                if computed == None:
                    new_line.append(macro_val)
                else:
                    new_line.append(computed)
            else:
                new_line.append(word)
                not_changed_counter += 1
    if len(words) == not_changed_counter:
        return line
    else:
        return reduce(lambda x,y: x+' '+y+' ',new_line)
            
            
def pass_values(lines,macro_table):
    result = []
    for line in lines:
        new_line = pass_value(line,macro_table)
        if '$' in new_line:
            print(new_line)
            new_line = pass_value(new_line,macro_table)
        if new_line != None:
            result.append(new_line)
        else:
            result.append(line)
    return result

def write_result(file_path,lines):
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
   lines = match_macroses(file,macro_table)
   lines = pass_values(lines,macro_table)
   write_result(file,lines)
