import re

TK_NUM    = 'NUM'
TK_ID     = 'ID'
TK_PLUS   = 'PLUS'
TK_MINUS  = 'MINUS'
TK_MUL    = 'MUL'
TK_DIV    = 'DIV'
TK_LPAREN = 'LPAREN'
TK_RPAREN = 'RPAREN'
TK_LBRACE = 'LBRACE'    # Novo: { 
TK_RBRACE = 'RBRACE'    # Novo: } 
TK_ASSIGN = 'ASSIGN'    # O '=' sozinho 
TK_EQ     = 'EQ'        # O '==' de comparação 
TK_LT     = 'LT'        # < 
TK_GT     = 'GT'        # > 
TK_SEMI   = 'SEMI'      # ;
TK_COMMA  = 'COMMA'     # ,
TK_EOF    = 'EOF'

# Palavras que o compilador já conhece "de cor" 
KEYWORDS = {
    'var'    : 'VAR',
    'return' : 'RETURN',
    'if'     : 'IF',        
    'else'   : 'ELSE',      
    'while'  : 'WHILE',     
}

class Token:
    def __init__(self, type, value):
        self.type  = type
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {self.value!r})'

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos  = 0

    def error(self):
        ch = self.text[self.pos]
        raise SyntaxError(f'Caractere estranho: {ch!r} na posição {self.pos}')

    def peek(self):
        # Olha o próximo caractere sem "consumir" ele. Útil pro '==' 
        nxt = self.pos + 1
        return self.text[nxt] if nxt < len(self.text) else None

    def advance(self):
        # Pula pro próximo caractere
        ch = self.text[self.pos]
        self.pos += 1
        return ch

    def skip_whitespace(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

    def read_number(self):
        start = self.pos
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            self.pos += 1
        return Token(TK_NUM, int(self.text[start:self.pos]))

    def read_id_or_keyword(self):
        # Lê o nome e depois decide se é uma variável ou um comando (if/while) 
        start = self.pos
        while self.pos < len(self.text) and (self.text[self.pos].isalnum() or self.text[self.pos] == '_'):
            self.pos += 1
        word = self.text[start:self.pos]
        ttype = KEYWORDS.get(word, TK_ID)
        return Token(ttype, word)

    def next_token(self):
        self.skip_whitespace()

        if self.pos >= len(self.text):
            return Token(TK_EOF, None)

        ch = self.text[self.pos]

        # Números
        if ch.isdigit():
            return self.read_number()

        # Identificadores e Palavras-chave
        if ch.isalpha() or ch == '_':
            return self.read_id_or_keyword()

        # A lógica crítica: '=' vs '==' 
        if ch == '=':
            if self.peek() == '=':
                self.pos += 2 # Pula os dois '='
                return Token(TK_EQ, '==')
            else:
                self.pos += 1 # Pula só o '='
                return Token(TK_ASSIGN, '=')

        # Operadores simples e pontuação
        self.pos += 1
        simple = {
            '+': TK_PLUS,
            '-': TK_MINUS,
            '*': TK_MUL,
            '/': TK_DIV,
            '(': TK_LPAREN,
            ')': TK_RPAREN,
            '{': TK_LBRACE,
            '}': TK_RBRACE,
            '<': TK_LT,
            '>': TK_GT,
            ';': TK_SEMI,
            ',': TK_COMMA,
        }
        
        if ch in simple:
            return Token(simple[ch], ch)

        # Se chegou aqui e não reconheceu nada, deu ruim
        self.pos -= 1
        self.error()

    def tokenize(self):
        """Gera a lista completa de tokens de uma vez"""
        tokens = []
        while True:
            tok = self.next_token()
            tokens.append(tok)
            if tok.type == TK_EOF:
                break
        return tokens