# -*- coding: utf-8 -*-

import re

from chasm.errors import Logger

logger = Logger()

asm_tokens = [
    {'type': 'T_LABEL', 'pattern': r'([a-zA-Z_]{3}[\w\d_]*)\:'},
    {'type': 'T_COMMAND', 'pattern': r'(SYS|CLS|RET|JP|CALL|'
     'SE|SNE|LD|ADD|OR|AND|XOR|SUBN|SUB|SHR|SHL|SNE|'
     'RND|DRW|SKP|SKNP|DW|DB|SCD|SCR|SCL|EXIT|LOW|HIGH)'},
    {'type': 'T_NAME', 'pattern': r'^([a-zA-Z_]{3}[\w\d_]*)'},
    {'type': 'T_DELAY', 'pattern': r'DT'},
    {'type': 'T_SOUND', 'pattern': r'ST'},
    {'type': 'T_BINARY', 'pattern': r'B'},
    {'type': 'T_FONT', 'pattern': r'F'},
    {'type': 'T_KEYBOARD', 'pattern': r'K'},
    {'type': 'T_HIGH_FONT', 'pattern': r'HF'},
    {'type': 'T_FLAG', 'pattern': r'R'},
    {'type': 'T_MEMORY_I', 'pattern': r'\[I\]'},
    {'type': 'T_REGISTER_I', 'pattern': r'I'},
    {'type': 'T_WORD', 'pattern': r'(0x|#)?[\da-fA-F]{4}'},
    {'type': 'T_ADDR', 'pattern': r'(0x|#)?[\da-fA-F]{3}'},
    {'type': 'T_BYTE', 'pattern': r'(0x|#)?[\da-fA-F]{2}'},
    {'type': 'T_NIBBLE', 'pattern': r'(0x|#)?[\da-fA-F]{1}'},
    {'type': 'T_REGISTER', 'pattern': r'V[\da-fA-F]{1}'},
    {'type': 'T_COMMENT', 'pattern': r'^;[^\n]*'},
    {'type': 'T_COMMA', 'pattern': r','},
    {'type': 'T_WHITESPACE', 'pattern': r'^[ \t\r]'},
    {'type': 'T_EOL', 'pattern': r'^\n'},
    {'type': 'T_UNKNOW', 'pattern': r'[:punct:#\d\w]+'}
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

        if token['class'] == 'T_UNKNOW':
            logger.fail("Invalid token {0} in ({1}, {2})",
                        token['lexeme'], line, column)

        tokens.append({'class': token['class'],
                       'lexeme': token['lexeme'],
                       'line': line,
                       'column': column})

        if token['class'] == 'T_EOL':
            line, column = (line + 1, 1)
        else:
            column += token['size']

        code = code[token['size']:]
    return tokens
