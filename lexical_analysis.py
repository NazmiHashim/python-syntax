import re

alphabet = re.compile(r'[a-zA-Z]')
digit = re.compile(r'\d')
operator = re.compile(r'[+\-*/^|=]')
punctuator = re.compile(r'[(){}[\];:\'"]')

# Token class represents a lexical token with a type and value.
class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

# Lexer class tokenizes the input code.
class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.current_char = self.code[self.position]

    def advance(self):
        # Move to the next character in the code.
        self.position += 1
        if self.position > len(self.code) - 1:
            self.current_char = None
        else:
            self.current_char = self.code[self.position]

    def skip_whitespace(self):
        # Skip over whitespace characters.
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        # Extract an integer from the code.
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def identifier(self):
        # Extract an identifier from the code (alphanumeric characters and underscores).
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char in {'_', '.'}):
            result += self.current_char
            self.advance()
        return result

    def categorize_token(self, keywords, letters, numbers, operators, punctuators, others):
        if self.current_char is None:
            return None

        if alphabet.match(self.current_char):
            # If the character is alphabetic, extract an identifier.
            token_value = self.identifier()

            if token_value in {'return', 'print'}:
                keywords.append(token_value)
                return Token('KEYWORD', token_value)
            else:
                letters.append(token_value)
                return Token('IDENTIFIER', token_value)
        
        elif digit.match(self.current_char):
            # If the character is a digit, extract an integer.
            token_value = str(self.integer())
            numbers.append(token_value)
            return Token('INTEGER', token_value)
        
        elif operator.match(self.current_char):
            # If the character is an operator, categorize it as an operator.
            token_value = self.current_char
            operators.append(token_value)
            self.advance()
            return Token('OPERATOR', token_value)
        
        elif punctuator.match(self.current_char):
            # If the character is a punctuator, categorize it as a punctuator.
            token_value = self.current_char
            self.advance()
            punctuators.append(token_value)

            return Token('PUNCTUATOR', token_value)
        
        elif re.match(r'[!@#$%&_<>\?]', self.current_char):
            # If the character matches a specific pattern, categorize it as "OTHER".
            token_value = self.current_char
            others.append(token_value)
            self.advance()
            return Token('OTHER', token_value)
        else:
            # If the character doesn't match any category, simply advance to the next character.
            self.advance()


    def get_tokens(self):
        keywords = []
        letters = []
        numbers = []
        operators = []
        punctuators = []
        others = []

        while self.current_char is not None:
                token = self.categorize_token(keywords, letters, numbers, operators, punctuators, others)
                if token:
                    yield token

        return letters, numbers, operators, punctuators, others


    

 
