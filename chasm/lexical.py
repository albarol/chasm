# -*- coding: utf-8 -*-

import re

from chasm.errors import Logger

logger = Logger()

asm_tokens = [
    { 'type': 'TOKEN_LABEL', 'pattern': r'([\w]{2}[\w\d_]*)\:'},
    { 'type': 'TOKEN_COMMAND', 'pattern': r'(SYS|CLS|RET|JP|CALL|'
                                 'SE|SNE|LD|ADD|OR|AND|'
                                 'XOR|SUBN|SUB|SHR|SHL|SNE|'
                                 'RND|DRW|SKP|SKNP|DW|DB|'
                                 'SCD|SCR|SCL|EXIT|LOW|HIGH)'},
    { 'type': 'TOKEN_WORD', 'pattern': r'0x[\da-fA-F]{4}'},
    { 'type': 'TOKEN_ADDR', 'pattern': r'0x[\da-fA-F]{3}'},
    { 'type': 'TOKEN_BYTE', 'pattern': r'0x[\da-fA-F]{2}'},
    { 'type': 'TOKEN_NIBBLE', 'pattern': r'0x[\da-fA-F]{1}'},
    { 'type': 'TOKEN_VALUE', 'pattern': r'^[0-9]{1,3}'},
    { 'type': 'TOKEN_NAME', 'pattern': r'^([\w]{3}[\w\d]*)'},
    { 'type': 'TOKEN_REGISTER', 'pattern': r'V[\da-fA-F]{1}'},
    { 'type': 'TOKEN_DELAY', 'pattern': r'DT'},
    { 'type': 'TOKEN_SOUND', 'pattern': r'ST'},
    { 'type': 'TOKEN_BINARY', 'pattern': r'B'},
    { 'type': 'TOKEN_FONT', 'pattern': r'F'},
    { 'type': 'TOKEN_KEYBOARD', 'pattern': r'K'},
    { 'type': 'TOKEN_HIGH_FONT', 'pattern': r'HF'},
    { 'type': 'TOKEN_FLAG', 'pattern': r'R'},
    { 'type': 'TOKEN_MEMORY_I', 'pattern': r'\[I\]'},
    { 'type': 'TOKEN_REGISTER_I', 'pattern': r'I'},
    { 'type': 'TOKEN_COMMENT', 'pattern': r'^;[^\n]*'},
    { 'type': 'TOKEN_COMMA', 'pattern': r','},
    { 'type': 'TOKEN_WHITESPACE', 'pattern': r'^[ \t\r]'},
    { 'type': 'TOKEN_EOL', 'pattern': r'^\n'},
    { 'type': 'TOKEN_UNKNOW', 'pattern': r'[:punct:#\d\w]+'}
]


def tokenize(code):
    tokens = []
    line, column = (1, 1)
    while len(code) > 0:
        for token in asm_tokens:
            match = re.match(token['pattern'], code, re.S)
            if match:
                if token['type'] == 'TOKEN_UNKNOW':
                    logger.fail("Invalid token %s in (%s, %s)" %
                               (match.group(0), line, column))

                tokens.append({'type': token['type'],
                               'value': match.group(0),
                               'line': line,
                               'column': column})

                if token['type'] == 'TOKEN_EOL':
                    line += 1
                    column = 1
                else:
                    column += len(match.group(0))

                code = code[len(match.group(0)):]
                break
    return tokens
