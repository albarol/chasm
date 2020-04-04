# -*- coding: utf-8 -*-

from chasm.errors import Logger

logger = Logger()

rules = {
    'SYS': [('T_COMMAND', 'T_NUMBER'),
            ('T_COMMAND', 'T_CONSTANT'),
            ('T_COMMAND', 'T_NAME')],
    'CLS': [('T_COMMAND',)],
    'RET': [('T_COMMAND',)],
    'JP':  [('T_COMMAND', 'T_NAME'),
            ('T_COMMAND', 'T_CONSTANT'),
            ('T_COMMAND', 'T_NUMBER'),
            ('T_COMMAND', 'T_NAME'),
            ('T_COMMAND', 'T_CONSTANT', 'T_COMMA', 'T_REGISTER'),
            ('T_COMMAND', 'T_NUMBER', 'T_COMMA', 'T_REGISTER'),
            ('T_COMMAND', 'T_NAME', 'T_COMMA', 'T_REGISTER')],
    'CALL': [('T_COMMAND', 'T_CONSTANT'),
             ('T_COMMAND', 'T_NUMBER'),
             ('T_COMMAND', 'T_NAME')],
    'SE': [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER'),
           ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_NUMBER'),
           ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_NAME'),
           ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_CONSTANT')],
    'SNE': [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_NUMBER'),
            ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_NAME'),
            ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_CONSTANT'),
            ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER')],
    'ADD': [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_CONSTANT'),
            ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_NUMBER'),
            ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_NAME'),
            ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER'),
            ('T_COMMAND', 'T_REGISTER_I', 'T_COMMA', 'T_REGISTER')],
    'OR':  [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER')],
    'AND':  [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER')],
    'XOR':  [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER')],
    'SUB':  [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER')],
    'SHR':  [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER'),
             ('T_COMMAND', 'T_REGISTER')],
    'SUBN':  [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER')],
    'SHL':  [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER'),
             ('T_COMMAND', 'T_REGISTER')],
    'RND': [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_NUMBER'),
            ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_CONSTANT'),
            ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_NAME')],
    'DRW': [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER', 'T_COMMA', 'T_NUMBER'),
            ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER', 'T_COMMA', 'T_NAME'),
            ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER', 'T_COMMA', 'T_CONSTANT')],
    'SKP': [('T_COMMAND', 'T_REGISTER')],
    'SKNP': [('T_COMMAND', 'T_REGISTER')],
    'LD': [('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_REGISTER'),
           ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_CONSTANT'),
           ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_NUMBER'),
           ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_NAME'),
           ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_DELAY'),
           ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_KEYBOARD'),
           ('T_COMMAND', 'T_DELAY', 'T_COMMA', 'T_REGISTER'),
           ('T_COMMAND', 'T_SOUND', 'T_COMMA', 'T_REGISTER'),
           ('T_COMMAND', 'T_REGISTER_I', 'T_COMMA', 'T_CONSTANT'),
           ('T_COMMAND', 'T_REGISTER_I', 'T_COMMA', 'T_NUMBER'),
           ('T_COMMAND', 'T_REGISTER_I', 'T_COMMA', 'T_NAME'),
           ('T_COMMAND', 'T_MEMORY_I', 'T_COMMA', 'T_REGISTER'),
           ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_MEMORY_I'),
           ('T_COMMAND', 'T_FONT', 'T_COMMA', 'T_REGISTER'),
           ('T_COMMAND', 'T_BINARY', 'T_COMMA', 'T_REGISTER'),
           ('T_COMMAND', 'T_HIGH_FONT', 'T_COMMA', 'T_REGISTER'),
           ('T_COMMAND', 'T_FLAG', 'T_COMMA', 'T_REGISTER'),
           ('T_COMMAND', 'T_REGISTER_I', 'T_COMMA', 'T_NAME'),
           ('T_COMMAND', 'T_REGISTER', 'T_COMMA', 'T_FLAG')
           ],
    'DW': [('T_COMMAND', 'T_NUMBER'),
           ('T_COMMAND', 'T_CONSTANT')],
    'DB': [('T_COMMAND', 'T_NUMBER'),
           ('T_COMMAND', 'T_CONSTANT')],
    'SCD': [('T_COMMAND', 'T_NUMBER'),
            ('T_COMMAND', 'T_CONSTANT'),
            ('T_COMMAND', 'T_NAME')],
    'SCR': [('T_COMMAND',)],
    'SCL': [('T_COMMAND',)],
    'EXIT': [('T_COMMAND',)],
    'LOW': [('T_COMMAND',)],
    'HIGH': [('T_COMMAND',)]
}


def analyze(ast):
    for addr, node in ast.nodes.items():
        check_instruction(node)
        lookup_symbols(node, ast.symbols)
        check_memory_address(node)
    return True


def check_instruction(node):
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


def check_memory_address(node):
    tokens = filter(lambda t: t['class'] in ['T_NUMBER', 'T_CONSTANT'], node)
    command = node[0]['lexeme']
    begin, end = 0x200, 0xFFF

    for token in tokens:
        address = int(token['lexeme'], 16)

        use_addr = command in ('JP', 'CALL') or (command == 'LD' and node[1]['lexeme'] == 'T_REGISTER_I')

        if address < begin and use_addr:
            logger.warning("Invalid memory address {0} in ({1}, {2})",
                           hex(address), token['line'], token['column'])

        if address > end and command not in ('DW'):
            logger.fail("Invalid memory address {0} in ({1}, {2})",
                        hex(address), token['line'], token['column'])
