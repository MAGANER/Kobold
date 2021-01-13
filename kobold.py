#Kobold is meta-language used to improve the view of source code
#or even to create completely new language based on another one!
#exampe of use:$python kobold.py source1.cpp source2.cpp header1.h macro.ko
#syntax of Kobold is pretty simple
#macro   -> expr
#macro_n -> expr
#Also there is an ability to generate expression
#macro = {n,expr} some another expression
#Instead of macro there will be expression duplicated n times
#Let imagine the moment, where you don't need macro, but
#if you write it, you get the expression of macro
#so you can write this: 'macro' and this macro won't be computed
#but if you need to pass macro result between quotes?
#then you need to write just ''macro'' and you will get 'result'
#Also macro can take args:
#Common syntax:
#macro# -> some expression #0 and #1, so also write #2
#so #n means pass argument n if it exists
#it can be use in generative expressions as well:
# {6, #3 }

import sys
from functools import reduce

#functions to get data to process
def get_files():
    return sys.argv[1:]
def separate(files):
    '''separates terminal arguments to get sources and macro file'''
    macro_file = ""
    sources    = []
    options    = []
    for f in files:
        if ".ko" in f and len(macro_file) == 0:
            macro_file = f
        elif ".ko" in f:
            print(f"can not get more than 1 macro file {f} is not allowed!")
            exit(-1)
        elif f[0] == '-':
            options.append(f)
            
        if ".ko" not in f and f[0] != '-':
            sources.append(f)
    if len(macro_file) == 0 and '-oo' not in options:
        print("you should pass macro file!")
        exit(-1)

    return (macro_file,sources,options)
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
def _match_macro(macro_table,line):
    '''set all macro values into the line'''
    new_line = []
    words = line.split(' ')
    
    def generate_macro(word,macro_table):
        '''sub function to compute macro
           there can be some expression
           so it must be checked
        '''
        computed = compute_generative_expression(macro_table[word],macro_table)
        val_to_set = ""
        if computed != None:
            val_to_set = computed
        else:
            val_to_set = macro_table[word]
        return val_to_set
    
    for word in words:
        not_empty = len(word) > 0
        pass_val_embraced_with_quotes = word[0:2] == "''" and word[len(word)-2:] == "''"
        word_with_no_quotes = word[2:len(word)-2]
        if not_empty and word in macro_table:
            value = generate_macro(word,macro_table)
            new_line.append(value)
        elif not_empty and pass_val_embraced_with_quotes and word_with_no_quotes in macro_table:
            value = generate_macro(word_with_no_quotes,macro_table)
            new_line.append(f"'{value}'")
        elif not_empty and word not in macro_table:
            new_line.append(word)
            
    return reduce(lambda x,y:x+' '+y+' ',new_line)
def match_macroses(file_path,macro_table):
    '''process all files'''
    lines = []
    with open(file_path,"r") as f:
        for line in f:
            matched = _match_macro(macro_table,line)
            if matched == None:
                lines.append(line)
            else:
                lines.append(matched)
    return lines

def pass_value(line,macro_table):
    '''pass the value of macro into another one'''
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
    '''find all macroses in expressions and pass their value'''
    result = []
    for line in lines:
        new_line = pass_value(line,macro_table)
        if '$' in new_line:
            new_line = pass_value(new_line,macro_table)
        if new_line != None:
            result.append(new_line)
        else:
            result.append(line)
    return result

def compute_functional_macro_expression(args,macro_expr):
    '''pass argument values and also compute it'''
    result = ''
    words = macro_expr.split(' ')
    for word in words:
        if len(word) > 0 and word[0] == '#':
            word_as_list = list(word[1:])
            if len(word_as_list) > 0:
                arg_number = int(word[1:])
                if arg_number > len(args) or arg_number < 0:
                    result += ' '
                else:
                    #for example len = 2 and you pass 2 as argument number
                    #so you will get error
                    #prevent it
                    if arg_number < len(args):
                        result += args[arg_number]
        else:
            result+= f" {word} "
    result = result.replace('  ',' ')
    return result
def compute_functional_macro(line,macro_table):
    '''find and compute all functional macroses in line'''
    words = line.split(' ')
    results = []
    counter = 0
    not_changed_counter = 0
    while counter < len(words):
        word = words[counter]
        #find arguments' list

        open_brace = -1
        close_brace= -1
        macro_name = ''
        if '[' in word and ']' in word:
            open_brace = word.index('[')
            if open_brace != -1:
                close_brace = word.index(']')

                #check does such macro exist
                macro_name = word[:open_brace]+'#'
                exist = macro_name in macro_table
                if not exist:
                    not_changed_counter += 1
                    counter += 1
                    continue

                #go to the next word if there are no braces
                if open_brace == -1 or close_brace == -1:
                    not_changed_counter += 1
                    counter += 1
                    continue

            #get arguments
            arg_line = word[open_brace+1:close_brace]
            args = arg_line.split(',')
        
            #pass arguments
            expr = macro_table[macro_name]
            sub_result = compute_functional_macro_expression(args,expr)
            sub_result = compute_generative_expression(sub_result,macro_table)
            sub_result = compute_functional_macro_expression(args,sub_result)
            results.append(sub_result)
            
            counter += 1
        else:
            not_changed_counter += 1
            counter += 1

    if not_changed_counter == len(words):
        return line
    else:
        return reduce(lambda x,y:x+' '+y+' ',results)
        
def compute_functional_macroses(lines,macro_table):
    '''macro can take arguments'''
    result = []
    for line in lines:
        resulting_line = compute_functional_macro(line,macro_table)
        result.append(resulting_line)
    return result


#option processing
def erase_all(lines, val_to_erase):
    ''' delete every passed value in each line'''
    result = []
    for line in lines:
        result.append(line.replace(val_to_erase,''))
    return result 
def get_option_data(option):
    '''return pair of name and name, if it exists'''
    _option = ''
    val = ''
    if '=' not in option:
        _option = option[1:]
    else:
        eq = option.index('=')
        _option = option[1:eq]
        val = option[eq+1:]
    return (_option,val)
def process_options(options,lines):
    '''apply option function to file data'''
    result = lines
    for option in options:
        data = get_option_data(option)
        if data[0] == 'ea':
            result = erase_all(result,data[1])
    return result
####

def write_result(file_path,lines):
    with open(file_path,"w") as f:
        f.seek(0)
        f.truncate()

        for line in lines:
            f.write(line)        



files = separate(get_files())
macro_file = files[0]
files_to_change = files[1]
options = files[2]

#there is an ability to apply options only to file
#so check is this ability active
macro_table = {}
if "-oo" not in options:
    macro_table= parse(read(macro_file))

#-s options says it's needed to save original file version
#before applying any change
if "-s" in options:
    for file in files_to_change:
        lines = read(file)
        write_result(file.replace('.','original.'),lines)
    
lines = []
for file in files_to_change:
   #if only options ability is on
   #file must be loaded
   if "-oo" in options:
       lines = read(file)
    
   lines = match_macroses(file,macro_table)
   lines = pass_values(lines,macro_table)
   lines = compute_functional_macroses(lines,macro_table)
   if len(options) > 0:
       lines = process_options(options,lines)
   write_result(file,lines)
