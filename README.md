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

Macros will be replaced with expression.<br/>
To run processor you pass files and macro file with .ko extension as argv:<br/>
***python kobold.py source1 source2 source_n macroses.ko***

Task list:
- [x] - made basical macro-processor
- [ ] - add an support of regular expression for macro expressions
