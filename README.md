# Kobold
macro-processor

This is simple macro-processor can be used for simple text replacing, but 
also there can be complex expression computed before string replacing.

# Syntax
In common way:

***macro1 -> expression<br/>
macron -> expression_n***

Macros will be replaced with expression.<br/>
To run processor you pass files and macro file with .ko extension as argv:<br/>
***python kobold.py source1 source2 source_n macroses.ko***

Task list:
- [x] - made basical macro-processor
- [ ] - add an support of regular expression for macro expressions
