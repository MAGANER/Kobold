# Kobold
macro-processor

This is simple macro-processor can be used for simple text replacing, but<br/>
also there can be complex expression computed before string replacing.<br/>
As an additional ability it has amount of optional functions.(Some of functions are planned only)<br/>

# Syntax
In common way:<br/>
(Also it's good to leave space in the end of the line)

***macro1 -> expression<br/>
macron -> expression_n***

There is kind of generative expressions:<br/>
***macro -> hello, {4, world }<br/>***
You will get hello and  world repeated 4 times.

Also you can pass value of macro into the another one:<br/>
***macro1 -> some expression and $macron***<br/>
Also macron will be computed and passed to its place.

So, but if you need to write macro name, but don't use this macro?<br/>
embrace it with ':<br/>
***'macro'***<br/>
and this macro won't be computed.

But if you need to pass result of macro into '?<br/>
Not problem. Type something like this:<br/>
***''macro''***<br/>
So you get ***'macro_result'***

Now i want to show functional macro:<br/>
In common way it looks so:<br/>
***macro# -> some word is #0 and you know what is #1<br/>***
In file write:***macro[arg0, arg1]***

Also when you use argument you must split with space<br/>
And every macro must be ended with space!

# Options
There are bunch of functions and you can apply them to files:<br/>
All of the starts with -<br/>

List:<br/>
1. -oo means option only. So you can use optional functions only<br/>
2. -ea means erase all. Also you need to pass = after and value to erase<br/>
Example:***-ea=rep***<br/>
3. -s means save file copy before any change.<br/>
4. -c means count all elements in file and print where it is.<br/>
5. -ra means replace all old strings to the new ones<br/>
Example:***-ra=old:new***


Macros will be replaced with expression.<br/>
To run processor you pass files and macro file with .ko extension as argv:<br/>
***python kobold.py source1 source2 source_n macroses.ko***

## Task list:
- [x] - made basical macro-processor
- [ ] - add an support of regular expression for macro expressions
