
import re

TOKEN_REGEX = [
    ("NUMBER", r"[0-9]+"),
    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("TIMES", r"\*"),
    ("DIV", r"/"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("SKIP", r"[ \t\n]+"),
]

def tokenize(code):
    tokens = []
    pos = 0
    while pos < len(code):
        match = None
        for token_type, regex in TOKEN_REGEX:
            pattern = re.compile(regex)
            match = pattern.match(code, pos)
            if match:
                text = match.group(0)
                if token_type != "SKIP":
                    tokens.append((token_type, text))
                pos = match.end(0)
                break
        if not match:
            raise SyntaxError(f"Caractere inesperado: {code[pos]}")
    return tokens
