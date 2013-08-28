import re

from chasm.errors import Logger

logger = Logger()

asm_tokens = [
    { 'type': 'T_LABEL', 'pattern': r'([\w]{2}[\w\d_]*)\:'},
    { 'type': 'T_COMMAND', 'pattern': r'(SYS|CLS|RET|JP|CALL|'
                                 'SE|SNE|LD|ADD|OR|AND|'
                                 'XOR|SUBN|SUB|SHR|SHL|SNE|'
                                 'RND|DRW|SKP|SKNP|DW|DB|'
                                 'SCD|SCR|SCL|EXIT|LOW|HIGH)'},
    { 'type': 'T_WORD', 'pattern': r'#[\da-fA-F]{4}'},
    { 'type': 'T_ADDR', 'pattern': r'#[\da-fA-F]{3}'},
    { 'type': 'T_BYTE', 'pattern': r'#[\da-fA-F]{2}'},
    { 'type': 'T_NIBBLE', 'pattern': r'#[\da-fA-F]{1}'},
    { 'type': 'T_VALUE', 'pattern': r'^[0-9]{1,3}'},
    { 'type': 'T_NAME', 'pattern': r'^([\w]{3}[\w\d]*)'},
    { 'type': 'T_REGISTER', 'pattern': r'V[\da-fA-F]{1}'},
    { 'type': 'T_DELAY', 'pattern': r'DT'},
    { 'type': 'T_SOUND', 'pattern': r'ST'},
    { 'type': 'T_BINARY', 'pattern': r'B'},
    { 'type': 'T_FONT', 'pattern': r'F'},
    { 'type': 'T_KEYBOARD', 'pattern': r'K'},
    { 'type': 'T_HIGH_FONT', 'pattern': r'HF'},
    { 'type': 'T_FLAG', 'pattern': r'R'},
    { 'type': 'T_MEMORY_I', 'pattern': r'\[I\]'},
    { 'type': 'T_REGISTER_I', 'pattern': r'I'},
    { 'type': 'T_COMMENT', 'pattern': r'^;(.*)[^\n]'},
    { 'type': 'T_WHITESPACE', 'pattern': r'^[ \t\r]'},
    { 'type': 'T_COMMA', 'pattern': r','},
    { 'type': 'T_EOL', 'pattern': r'^\n'},
    { 'type': 'T_UNKNOW', 'pattern': r'[:punct:#\d\w]+'}
]


def tokenize(code):
    tokens = []
    line, column = (1, 1)
    while len(code) > 0:
        for token in asm_tokens:
            match = re.match(token['pattern'], code, re.S)
            if match:
                if token['type'] == 'T_UNKNOW':
                    logger.fail("Invalid token %s in (%s, %s)" %
                               (match.group(0), line, column))

                tokens.append({'type': token['type'],
                               'value': match.group(0),
                               'line': line,
                               'column': column})

                if token['type'] == 'T_EOL':
                    line += 1
                    column = 1
                else:
                    column += len(match.group(0))

                code = code[len(match.group(0)):]
                break
    return tokens
