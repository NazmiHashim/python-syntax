# Group assignment for CPT316

### Group Member
1) MOHAMAD NAZMI BIN HASHIM 158616 
2) MIOR MUHAMMAD IRFAN BIN MIOR LATFEE 158450 
3) OOI JING MIN 158768 
4) MUNIRAH BINTI SHAMSUDIN 157518 
5) SHONEERA SIMIN 159160
   
## Lexical and Syntax Analysis program

This program is a pyhton-based lexical and syntax analyzer is designed to identify and analyze the structure of the code. It initially divides the input into tokens via lexical analysis and then applies syntax analysis to determine whether the code is correctly structured and complies with the required grammatical rules. An Abstract Syntax Tree (AST) is generated as the outcome of the successful syntax analysis.

## How it Work
Put it all file in the same folder and run file main.py in your python console:

### Input:
```
x=x+y
```

### Output for Tokenizing
```
Token Information:
Token Type: IDENTIFIER, Token Value: x
Token Type: OPERATOR, Token Value: =
Token Type: IDENTIFIER, Token Value: x
Token Type: OPERATOR, Token Value: +
Token Type: IDENTIFIER, Token Value: y
```

### Resulting Abstract Syntax Tree (AST):

```
Abstract Syntax Tree:
=:OPERATOR
        x:IDENTIFIER
        +:OPERATOR
                x:IDENTIFIER
                y:IDENTIFIER
```

#### This program enables you to enter multiple times of expression unless type exit to end the program

## Import Function
're' (Regular Expression Operation) :used for defining patterns to match characters in input during lexical analysis

## Features





