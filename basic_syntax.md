## BASIC syntax

### Generalized language

Note: `--` indicates a comment, `<CR>` indicates a carriage return (i.e. newline), and `[]` indicates optional elements.

```
-- Value tokens (Number supports floating point values)
VALUE = NUMBER | STRING | IDENTIFIER
NUMBER = [0-9]+.?[0-9]* | [0-9]+
STRING = '"' [^"]* '"'
IDENTIFIER = [a-zA-Z_][a-zA-Z0-9_]*

-- Operators
OPERATOR = '+' | '-' | '*' | '/' | '=' | '<' | '>' | '<=' | '>=' | '!='

-- Expressions
EXPRESSION = VALUE | IDENTIFIER | OPERATOR_EXPRESSION
OPERATOR_EXPRESSION = VALUE OPERATOR VALUE | IDENTIFIER OPERATOR IDENTIFIER | '(' EXPRESSION ')'

-- Keywords
KW_IF = 'IF'
KW_THEN = 'THEN'
KW_ELSE = 'ELSE'
KW_WHILE = 'WHILE'
KW_GOTO = 'GOTO'
KW_DO = 'DO'
KW_PRINT = 'PRINT'
KW_LET = 'LET'
KW_END = 'END'
KW_REM = 'REM'

-- Program structure
PROGRAM = LINES
LINES = LINE <CR> [LINES]
LINE = LINE_NUMBER STATEMENT
LINE_NUMBER = NUMBER

-- Statements
STATEMENT = ASSIGNMENT | PRINT_STATEMENT | IF_STATEMENT | WHILE_STATEMENT | REM_STATEMENT | GOTO_STATEMENT
ASSIGNMENT = KW_LET IDENTIFIER '=' EXPRESSION
PRINT_STATEMENT = KW_PRINT '(' EXPRESSION ')'
IF_STATEMENT = KW_IF '(' EXPRESSION ')' KW_THEN <CR> LINES [<CR> KW_ELSE <CR> LINES] KW_END
WHILE_STATEMENT = KW_WHILE '(' EXPRESSION ')' KW_DO <CR> LINES KW_END
REM_STATEMENT = KW_REM [\^^]*
GOTO_STATEMENT = KW_GOTO IDENTIFIER
```

### Example

```basic
10 LET A = 5
20 LET B = 10
30 IF A < B THEN
40 PRINT (A + B)
50 ELSE
60 PRINT (B - A)
70 END
```
