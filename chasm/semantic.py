# -*- coding: utf-8 -*-

from chasm.errors import Logger

logger = Logger()


rules = {
    'SYS': [('TOKEN_COMMAND', 'TOKEN_ADDR')],
    'CLS': [('TOKEN_COMMAND',)],
    'RET': [('TOKEN_COMMAND',)],
    'JP':  [('TOKEN_COMMAND', 'TOKEN_NAME'),
            ('TOKEN_COMMAND', 'TOKEN_ADDR'),
            ('TOKEN_COMMAND', 'TOKEN_ADDR', 'TOKEN_COMMA', 'TOKEN_REGISTER')],
    'CALL': [('TOKEN_COMMAND', 'TOKEN_ADDR'),
             ('TOKEN_COMMAND', 'TOKEN_NAME')],
    'SE': [('TOKEN_COMMAND', 'TOKEN_REGISTER', 'TOKEN_COMMA', 'TOKEN_REGISTER'),
           ('TOKEN_COMMAND', 'TOKEN_REGISTER', 'TOKEN_COMMA', 'TOKEN_BYTE')],
    'SNE': [('TOKEN_COMMAND', 'TOKEN_REGISTER', 'TOKEN_COMMA', 'TOKEN_BYTE'),
            ('TOKEN_COMMAND', 'TOKEN_REGISTER', 'TOKEN_COMMA', 'TOKEN_REGISTER')],
    'ADD': [('TOKEN_COMMAND', 'TOKEN_REGISTER', 'TOKEN_COMMA', 'TOKEN_BYTE'),
            ('TOKEN_COMMAND', 'TOKEN_REGISTER', 'TOKEN_COMMA', 'TOKEN_REGISTER'),
            ('TOKEN_COMMAND', 'TOKEN_REGISTER_I', 'TOKEN_COMMA', 'TOKEN_REGISTER')],
    'OR':  [('TOKEN_COMMAND', 'TOKEN_REGISTER', 'TOKEN_COMMA', 'TOKEN_REGISTER')],
    'AND':  [('TOKEN_COMMAND', 'TOKEN_REGISTER', 'TOKEN_COMMA', 'TOKEN_REGISTER')],
    'XOR':  [('TOKEN_COMMAND', 'TOKEN_REGISTER', 'TOKEN_COMMA', 'TOKEN_REGISTER')],
    'SUB':  [('TOKEN_COMMAND', 'TOKEN_REGISTER', 'TOKEN_COMMA', 'TOKEN_REGISTER')],
    'SHR':  [('TOKEN_COMMAND', 'TOKEN_REGISTER', 'TOKEN_COMMA', 'TOKEN_REGISTER')],
    'SUBN':  [('TOKEN_COMMAND', 'TOKEN_REGISTER', 'TOKEN_COMMA', 'TOKEN_REGISTER')],
    'SHL':  [('TOKEN_COMMAND', 'TOKEN_REGISTER', 'TOKEN_COMMA', 'TOKEN_REGISTER')],
    'RND': [('TOKEN_COMMAND', 'TOKEN_REGISTER', 'TOKEN_COMMA', 'TOKEN_BYTE')],
    'DRW': [('TOKEN_COMMAND', 'TOKEN_REGISTER', 'TOKEN_COMMA', 'TOKEN_REGISTER',
             'TOKEN_COMMA', 'TOKEN_NIBBLE')],
    'SKP': [('TOKEN_COMMAND', 'TOKEN_REGISTER')],
    'SKNP': [('TOKEN_COMMAND', 'TOKEN_REGISTER')],
    'LD': [('TOKEN_COMMAND', 'TOKEN_REGISTER', 'TOKEN_COMMA', 'TOKEN_REGISTER'),
           ('TOKEN_COMMAND', 'TOKEN_REGISTER', 'TOKEN_COMMA', 'TOKEN_BYTE'),
           ('TOKEN_COMMAND', 'TOKEN_REGISTER', 'TOKEN_COMMA', 'TOKEN_DELAY'),
           ('TOKEN_COMMAND', 'TOKEN_REGISTER', 'TOKEN_COMMA', 'TOKEN_KEYBOARD'),
           ('TOKEN_COMMAND', 'TOKEN_DELAY', 'TOKEN_COMMA', 'TOKEN_REGISTER'),
           ('TOKEN_COMMAND', 'TOKEN_SOUND', 'TOKEN_COMMA', 'TOKEN_REGISTER'),
           ('TOKEN_COMMAND', 'TOKEN_REGISTER_I', 'TOKEN_COMMA', 'TOKEN_ADDR'),
           ('TOKEN_COMMAND', 'TOKEN_MEMORY_I', 'TOKEN_COMMA', 'TOKEN_REGISTER'),
           ('TOKEN_COMMAND', 'TOKEN_REGISTER', 'TOKEN_COMMA', 'TOKEN_MEMORY_I'),
           ('TOKEN_COMMAND', 'TOKEN_FONT', 'TOKEN_COMMA', 'TOKEN_REGISTER'),
           ('TOKEN_COMMAND', 'TOKEN_BINARY', 'TOKEN_COMMA', 'TOKEN_REGISTER'),
           ('TOKEN_COMMAND', 'TOKEN_HIGH_FONT', 'TOKEN_COMMA', 'TOKEN_REGISTER'),
           ('TOKEN_COMMAND', 'TOKEN_FLAG', 'TOKEN_COMMA', 'TOKEN_REGISTER'),
           ('TOKEN_COMMAND', 'TOKEN_REGISTER_I', 'TOKEN_COMMA', 'TOKEN_NAME'),
           ('TOKEN_COMMAND', 'TOKEN_REGISTER', 'TOKEN_COMMA', 'TOKEN_FLAG')
           ],
    'DW': [('TOKEN_COMMAND', 'TOKEN_WORD')],
    'DB': [('TOKEN_COMMAND', 'TOKEN_BYTE')],
    'SCD': [('TOKEN_COMMAND', 'TOKEN_NIBBLE')],
    'SCR': [('TOKEN_COMMAND',)],
    'SCL': [('TOKEN_COMMAND',)],
    'EXIT': [('TOKEN_COMMAND',)],
    'LOW': [('TOKEN_COMMAND',)],
    'HIGH': [('TOKEN_COMMAND',)]
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
    tokens = filter(lambda t: t['class'] == 'TOKEN_NAME', node)
    for token in tokens:
        if token['lexeme'] not in symbols:
            logger.fail("Invalid symbol {0} in ({1}, {2})",
                        token['lexeme'], token['line'], token['column'])
        else:
            symbol = symbols[token['lexeme']]
            token['lexeme'] = hex(symbol)


def is_valid_memory_address(node):
    addr = filter(lambda t: t['class'] == 'TOKEN_ADDR', node)
    if addr and addr[0]['lexeme'] < '0x200':
        logger.warning("Invalid memory address {0} in ({1}, {2})",
                       addr[0]['lexeme'], addr[0]['line'], addr[0]['column'])
