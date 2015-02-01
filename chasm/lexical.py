# -*- coding: utf-8 -*-

import re

from chasm.errors import Logger

logger = Logger()

asm_tokens = [
    {'type': 'TOKEN_LABEL', 'pattern': r'([\w]{2}[\w\d_]*)\:'},
    {'type': 'TOKEN_COMMAND', 'pattern': r'(SYS|CLS|RET|JP|CALL|'
     'SE|SNE|LD|ADD|OR|AND|XOR|SUBN|SUB|SHR|SHL|SNE|'
     'RND|DRW|SKP|SKNP|DW|DB|SCD|SCR|SCL|EXIT|LOW|HIGH)'},
    {'type': 'TOKEN_WORD', 'pattern': r'0x[\da-fA-F]{4}'},
    {'type': 'TOKEN_ADDR', 'pattern': r'0x[\da-fA-F]{3}'},
    {'type': 'TOKEN_BYTE', 'pattern': r'0x[\da-fA-F]{2}'},
    {'type': 'TOKEN_NIBBLE', 'pattern': r'0x[\da-fA-F]{1}'},
    {'type': 'TOKEN_VALUE', 'pattern': r'^[0-9]{1,3}'},
    {'type': 'TOKEN_NAME', 'pattern': r'^([\w]{3}[\w\d]*)'},
    {'type': 'TOKEN_REGISTER', 'pattern': r'V[\da-fA-F]{1}'},
    {'type': 'TOKEN_DELAY', 'pattern': r'DT'},
    {'type': 'TOKEN_SOUND', 'pattern': r'ST'},
    {'type': 'TOKEN_BINARY', 'pattern': r'B'},
    {'type': 'TOKEN_FONT', 'pattern': r'F'},
    {'type': 'TOKEN_KEYBOARD', 'pattern': r'K'},
    {'type': 'TOKEN_HIGH_FONT', 'pattern': r'HF'},
    {'type': 'TOKEN_FLAG', 'pattern': r'R'},
    {'type': 'TOKEN_MEMORY_I', 'pattern': r'\[I\]'},
    {'type': 'TOKEN_REGISTER_I', 'pattern': r'I'},
    {'type': 'TOKEN_COMMENT', 'pattern': r'^;[^\n]*'},
    {'type': 'TOKEN_COMMA', 'pattern': r','},
    {'type': 'TOKEN_WHITESPACE', 'pattern': r'^[ \t\r]'},
    {'type': 'TOKEN_EOL', 'pattern': r'^\n'},
    {'type': 'TOKEN_UNKNOW', 'pattern': r'[:punct:#\d\w]+'}
]


def get_token(code):
    for token in asm_tokens:
        match = re.match(token['pattern'], code, re.S)
        if match:
            return {'class': token['type'],
                    'lexeme': match.group(0),
                    'size': len(match.group(0))}


def tokenize(code):
    tokens = []
    line, column = (1, 1)
    while len(code) > 0:
        token = get_token(code)

        if token['class'] == 'TOKEN_UNKNOW':
            logger.fail("Invalid token {0} in ({1}, {2})",
                        token['lexeme'], line, column)

        tokens.append({'class': token['class'],
                       'lexeme': token['lexeme'],
                       'line': line,
                       'column': column})

        if token['class'] == 'TOKEN_EOL':
            line, column = (line + 1, 1)
        else:
            column += token['size']

        code = code[token['size']:]
    return tokens
