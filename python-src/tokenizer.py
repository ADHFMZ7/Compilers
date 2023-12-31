from dataclasses import dataclass
from table import keywords
from error import report_token_error

@dataclass
class Token:
    lexeme: str
    type:   str
    line:   int

class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []

        self.start = 0
        self.current = 0
        self.line = 1

    def next_char(self):
        self.current += 1
        return self.source[self.current - 1]

    def peek(self):
        return self.source[self.current]

    def add_token(self, type):
        self.tokens.append(
                Token(self.substr(),
                      type,
                      self.line))
        self.start = self.current

    def substr(self):
        return self.source[self.start:self.current]

def tokenize_source(source: str):

    scanner = Scanner(source)

    while scanner.current < len(source) - 1:
        
        char = scanner.next_char()

        if scanner.source[scanner.current:len(scanner.source)].isspace():
            scanner.tokens.append(Token('$', '$', 0))
            return scanner.tokens

        while char.isspace():
            if char == '\n':
                scanner.line += 1
            scanner.start = scanner.current
            char = scanner.next_char()
        
        if char == "(":
            # Handles comments of the form (* COMMENT *)
            if scanner.peek() == '*':
                scanner.next_char()
                while scanner.next_char() != '*' and scanner.peek() != ')':
                    scanner.line += scanner.peek() == '\n'
                scanner.next_char()
                scanner.start = scanner.current
            else:
                scanner.add_token('(')

        elif char in "),;:=+-*/":
            #if not(scanner.peek().isnumeric()):
            scanner.add_token(char) 

        elif char == '"':
            scanner.next_char()
            while scanner.peek() != '"':
                if scanner.next_char() == '\n':
                    scanner.line += 1
            scanner.next_char()
            scanner.add_token("STRING")
            if scanner.peek() == ',':
                scanner.next_char()

        elif char.isalnum():
            while scanner.peek().isalnum():
                scanner.next_char()
        
            if scanner.substr() == "end" and scanner.peek() == '.':
                scanner.next_char()
            if scanner.substr() in keywords:
                scanner.add_token(scanner.substr()) 
            elif char.isalpha():
                scanner.add_token("IDENTIFIER")
            elif char.isnumeric():
                scanner.add_token("int")
                #scanner.tokens[-1].lexeme = str(int(scanner.tokens[-1].lexeme))
            else:
                report_token_error(scanner.substr(), scanner.line)

    scanner.tokens.append(Token('$', '$', 0))
    return scanner.tokens

