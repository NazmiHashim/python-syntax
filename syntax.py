class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    class ASTNode:
        def __init__(self, value, type, children=None):
            self.value = value
            self.type = type
            self.children = children or []

        def get_value(self):
            return self.value

        def get_type(self):
            return self.type

        def get_children(self):
            return self.children

    def consume(self):
        self.current_token_index += 1

    def get_current_token(self):
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None

    def parse(self):
        result = self.parse_statement()
        return result

    def parse_statement(self):
        current_token = self.get_current_token()

        if current_token is not None and current_token.type == 'IDENTIFIER':
            # Variable assignment statement
            variable_name = current_token.value
            self.consume()
            if self.get_current_token().type == 'OPERATOR' and self.get_current_token().value == '=':
                self.consume()  # Consume the '=' operator
                expression_node = self.parse_expression()
                return self.ASTNode('=', 'OPERATOR', [self.ASTNode(variable_name, 'IDENTIFIER'), expression_node])
            else:
                print("Error: Invalid statement -> Assignment operator '=' expected after variable name.")
        elif current_token is not None and current_token.type == 'KEYWORD' and current_token.value.lower() == 'print':
            # Print statement
            self.consume()  # Consume the 'print' keyword
            if self.get_current_token().type == 'PUNCTUATOR' and self.get_current_token().value == '(':
                self.consume()  # Consume the opening parenthesis
                expression_node = self.parse_expression()
                if self.get_current_token().type == 'PUNCTUATOR' and self.get_current_token().value == ')':
                    self.consume()  # Consume the closing parenthesis
                    return self.ASTNode('print', 'KEYWORD', [expression_node])
                else:
                    print("Error: Missing closing parenthesis ')' in print statement.")
            else:
                print("Error: Missing opening parenthesis '(' in print statement.")
        else:
            # Other statements (e.g., expressions, return statements)
            return self.parse_expression()

    def parse_expression(self):
        term_node = self.parse_high_precedence_term()
        return self.parse_expression_prime(term_node)

    def parse_expression_prime(self, left_node):
        current_token = self.get_current_token()

        while current_token is not None and current_token.type == 'OPERATOR' and current_token.value in {'+', '-', '=', '(', '[', '{', ')', ']', '}' }:
            self.consume()
            if current_token.value in {'(', '[', '{'}:
                # Handle parentheses, square brackets, and curly braces
                expression_node = self.parse_expression()
                closing_punctuator = {'(': ')', '[': ']', '{': '}'}
                if self.get_current_token().type == 'PUNCTUATOR' and self.get_current_token().value == closing_punctuator[current_token.value]:
                    self.consume()  # Consume the closing punctuator
                else:
                    print(f"Error: Mismatched {current_token.value} in expression")
                left_node = self.ASTNode(current_token.value, 'OPERATOR', [left_node, expression_node])
            else:
                term_node = self.parse_high_precedence_term()
                new_node = self.ASTNode(current_token.value, 'OPERATOR', [left_node, term_node])
                left_node = new_node
            current_token = self.get_current_token()

        return left_node
    
    def parse_high_precedence_term(self):
        factor_node = self.parse_factor()
        return self.parse_high_precedence_term_prime(factor_node)

    # Handle precedence for multiplication and division
    def parse_high_precedence_term_prime(self, left_node):
        current_token = self.get_current_token()

        while current_token is not None and current_token.type == 'OPERATOR' and current_token.value in {'*', '/'}:
            self.consume()
            factor_node = self.parse_factor()
            new_node = self.ASTNode(current_token.value, 'OPERATOR', [left_node, factor_node])
            left_node = new_node
            current_token = self.get_current_token()

        return left_node

    # Handle precedence for parentheses, square brackets, and curly braces
    def parse_factor(self):
        current_token = self.get_current_token()

        while current_token is not None and current_token.value.isspace():
            self.consume()
            current_token = self.get_current_token()

        if current_token is not None:
            if current_token.type in ['INTEGER', 'IDENTIFIER']:
                self.consume()
                return self.ASTNode(current_token.value, current_token.type)
            elif current_token.type == 'OTHER' and current_token.value.lower() == 'exit':
                self.consume()
                return self.ASTNode('exit', 'KEYWORD')  # Treat 'exit' as a special keyword
            elif current_token.type == 'KEYWORD' and current_token.value.lower() == 'return':
                self.consume()
                expression_node = self.parse_expression()
                return self.ASTNode('return', 'KEYWORD', [expression_node])
            elif current_token.type == 'PUNCTUATOR' and current_token.value == '{':
                # Handle curly braces
                self.consume()
                expression_node = self.parse_expression()
                if self.get_current_token().type == 'PUNCTUATOR' and self.get_current_token().value == '}':
                    self.consume()  # Consume the closing curly brace
                    return expression_node
                else:
                    print("Error: Mismatched curly braces in expression")
            elif current_token.type == 'PUNCTUATOR' and current_token.value == '[':
                # Handle square brackets
                self.consume()
                expression_node = self.parse_expression()
                if self.get_current_token().type == 'PUNCTUATOR' and self.get_current_token().value == ']':
                    self.consume() # Consume the closing square bracket
                    return expression_node
                else:
                    print("Error: Mismatched square brackets in expression")
            elif current_token.type == 'PUNCTUATOR' and current_token.value == '(':
                # Handle parentheses
                self.consume()
                expression_node = self.parse_expression()
                if self.get_current_token().type == 'PUNCTUATOR' and self.get_current_token().value == ')':
                    self.consume()  # Consume the closing parenthesis
                    return expression_node
                else:
                    print("Error: Mismatched parentheses in expression")
            else:
                print(f"Error: Invalid factor: Unexpected token type '{current_token.type}'")
        else:
            print("Error: Invalid factor: Unexpected end of input")

    # Print the resulting AST
    @staticmethod
    def print_ast(node, depth):
        if node is not None:
            for i in range(depth):
                print("\t", end="")
            node_type = 'KEYWORD' if node.get_type() == 'IDENTIFIER' and node.get_value() == 'exit' else node.get_type()
            print(node.get_value() + ":" + node_type)
            if node.get_children() is not None:
                for child in node.get_children():
                    Parser.print_ast(child, depth + 1)
