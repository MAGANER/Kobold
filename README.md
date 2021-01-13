# Kobold
macro-processor

This is simple macro-processor can be used for simple text replacing, but 
also there can be complex expression computed before string replacing.

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


Macros will be replaced with expression.<br/>
To run processor you pass files and macro file with .ko extension as argv:<br/>
***python kobold.py source1 source2 source_n macroses.ko***

Task list:
- [x] - made basical macro-processor
- [ ] - add an support of regular expression for macro expressions
