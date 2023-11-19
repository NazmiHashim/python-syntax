from lexical_analysis import Lexer
from syntax import Parser

def main():
    print('\nWelcome to lexical and syntax analysis program.')

    while True:
        # User input for the expression
        expression = input("\nEnter an expression (type 'exit' to end): ")
        if expression.lower() == 'exit':
            break  # Exit the loop if the user types 'exit'
        
        # Lexical analysis
        lexer = Lexer(expression)
        tokens = list(lexer.get_tokens())

        # Print token information
        print("\nToken Information:")
        for token in tokens:
            print(f'Token Type: {token.type}, Token Value: {token.value}')

        # Syntax analysis
        parser = Parser(tokens)
        ast = parser.parse()
        error = parser.get_error()

        # Print the resulting AST
        if(error):
            continue
        else:
            print("\nAbstract Syntax Tree:")
            Parser.print_ast(ast, 0)

if __name__ == "__main__":
    main()
