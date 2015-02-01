# -*- coding: utf-8 -*-

from chasm.errors import Logger

logger = Logger()


rules = {
    'SYS': [('T_COMMAND', 'T_ADDR')],
    'CLS': [('T_COMMAND',)],
    'RET': [('T_COMMAND',)],
    'JP':  [('T_COMMAND', 'T_NAME'),
            ('T_COMMAND', 'T_ADDR'),
            ('T_COMMAND', 'T_ADDR', 'T_COMMA', 'T_REGISTER')],
    'CALL': [('T_COMMAND', 'T_ADDR'),
             ('T_COMMAND', 'T_NAME')],
    'SE': [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER'),
           ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_BYTE')],
    'SNE': [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_BYTE'),
            ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER')],
    'ADD': [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_BYTE'),
            ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER'),
            ('T_COMMAND', 'T_REGISTER_I', 'T_COMMA', 'T_REGISTER')],
    'OR':  [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER')],
    'AND':  [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER')],
    'XOR':  [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER')],
    'SUB':  [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER')],
    'SHR':  [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER')],
    'SUBN':  [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER')],
    'SHL':  [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER')],
    'RND': [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_BYTE')],
    'DRW': [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER',
             'T_COMMA', 'T_NIBBLE')],
    'SKP': [('T_COMMAND', 'T_REGISTER')],
    'SKNP': [('T_COMMAND', 'T_REGISTER')],
    'LD': [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER'),
           ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_BYTE'),
           ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_DELAY'),
           ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_KEYBOARD'),
           ('T_COMMAND', 'T_DELAY', 'T_COMMA', 'T_REGISTER'),
           ('T_COMMAND', 'T_SOUND', 'T_COMMA', 'T_REGISTER'),
           ('T_COMMAND', 'T_REGISTER_I', 'T_COMMA', 'T_ADDR'),
           ('T_COMMAND', 'T_MEMORY_I', 'T_COMMA', 'T_REGISTER'),
           ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_MEMORY_I'),
           ('T_COMMAND', 'T_FONT', 'T_COMMA', 'T_REGISTER'),
           ('T_COMMAND', 'T_BINARY', 'T_COMMA', 'T_REGISTER'),
           ('T_COMMAND', 'T_HIGH_FONT', 'T_COMMA', 'T_REGISTER'),
           ('T_COMMAND', 'T_FLAG', 'T_COMMA', 'T_REGISTER'),
           ('T_COMMAND', 'T_REGISTER_I', 'T_COMMA', 'T_NAME'),
           ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_FLAG')
           ],
    'DW': [('T_COMMAND', 'T_WORD')],
    'DB': [('T_COMMAND', 'T_BYTE')],
    'SCD': [('T_COMMAND', 'T_NIBBLE')],
    'SCR': [('T_COMMAND',)],
    'SCL': [('T_COMMAND',)],
    'EXIT': [('T_COMMAND',)],
    'LOW': [('T_COMMAND',)],
    'HIGH': [('T_COMMAND',)]
}


def analyze(ast):
    for addr, node in ast.nodes.iteritems():
        is_valid_instruction(node)
        lookup_symbols(node, ast.symbols)
        is_valid_memory_address(node)
    return True


def is_valid_instruction(node):
    instruction = tuple([t['class'] for t in node])
    command = node[0]
    rule = rules[command['lexeme']]
    if instruction not in rule:
        instruction = ' '.join(map(lambda t: t['lexeme'], node))
        logger.fail("Invalid instruction {0} in ({1}, {2})",
                    instruction, command['line'], command['column'])


def lookup_symbols(node, symbols):
    tokens = filter(lambda t: t['class'] == 'T_NAME', node)
    for token in tokens:
        if token['lexeme'] not in symbols:
            logger.fail("Invalid symbol {0} in ({1}, {2})",
                        token['lexeme'], token['line'], token['column'])
        else:
            symbol = symbols[token['lexeme']]
            token['lexeme'] = hex(symbol)


def is_valid_memory_address(node):
    addr = filter(lambda t: t['class'] == 'T_ADDR', node)
    if addr and addr[0]['lexeme'] < '0x200':
        logger.warning("Invalid memory address {0} in ({1}, {2})",
                       addr[0]['lexeme'], addr[0]['line'], addr[0]['column'])
