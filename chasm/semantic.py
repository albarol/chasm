
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
    for node in ast.nodes:
        is_valid_instruction(node)
        lookup_symbols(node, ast.table)
        is_valid_memory_address(node)
    return True

def lookup_symbols(node, symbols):
  tokens = filter(lambda t: t['type'] == 'TOKEN_NAME', node)
  if tokens:
    token_name = tokens[0]
    if not token_name['value'] in symbols:
      logger.fail("Invalid symbol %s in (%s, %s)"
                  % (token_name['value'], node[0]['line'], node[0]['column']))
    else:
      symbol = symbols[token_name['value']]
      token_name['value'] = hex(symbol)


def is_valid_instruction(node):
    instruction = tuple([t['type'] for t in node])
    rule = rules[node[0]['value']]
    if not instruction in rule:
        instruction = ' '.join(map(lambda t: t['value'], node))
        logger.fail("Invalid instruction %s in (%s, %s)" % (instruction, node[0]['line'], node[0]['column']))
    return True

def is_valid_memory_address(node):
    addr = filter(lambda t: t['type'] == 'TOKEN_ADDR', node)
    if addr and addr[0]['value'] < '0x200':
        logger.warning("Invalid memory address %s in (%s, %s)"
              % (addr[0]['value'], addr[0]['line'], addr[0]['column']))
    return True
