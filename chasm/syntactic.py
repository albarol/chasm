# -*- coding: utf-8 -*-

from chasm.errors import Logger

logger = Logger()

grammar = {
    'T_SOL': ['T_LABEL', 'T_COMMAND'],
    'T_LABEL': ['T_EOL'],
    'T_COMMAND': ['T_REGISTER', 'T_BINARY', 'T_NIBBLE',
                      'T_ADDR', 'T_CONSTANT', 'T_DELAY',
                      'T_SOUND', 'T_FONT', 'T_REGISTER_I',
                      'T_BINARY', 'T_VALUE', 'T_WORD', 'T_EOL',
                      'T_NAME', 'T_MEMORY_I', 'T_HIGH_FONT', 'T_FLAG',
                      'T_BYTE'],
    'T_ADDR': ['T_EOL', 'T_COMMA'],
    'T_BYTE': ['T_EOL'],
    'T_NIBBLE': ['T_EOL'],
    'T_NAME': ['T_EOL'],
    'T_CONSTANT': ['T_EOL'],
    'T_VALUE': ['T_EOL'],
    'T_REGISTER': ['T_COMMA', 'T_EOL'],
    'T_DELAY': ['T_COMMA', 'T_EOL'],
    'T_SOUND': ['T_COMMA'],
    'T_BINARY': ['T_COMMA'],
    'T_FONT': ['T_COMMA'],
    'T_KEYBOARD': ['T_EOL'],
    'T_REGISTER_I': ['T_COMMA'],
    'T_MEMORY_I': ['T_COMMA', 'T_EOL'],
    'T_HIGH_FONT': ['T_COMMA'],
    'T_FLAG': ['T_COMMA', 'T_EOL'],
    'T_COMMA': ['T_REGISTER', 'T_BYTE', 'T_NIBBLE',
                    'T_DELAY', 'T_KEYBOARD', 'T_MEMORY_I',
                    'T_FLAG', 'T_ADDR', 'T_NAME'],
    'T_EOL': []
}


class Ast(object):

    def __init__(self, tokens):
        self.nodes = {}
        self.symbols = {}
        valid_tokens = filter(lambda token: token['class'] not in ('T_WHITESPACE', 'T_COMMENT'), tokens)
        self._generate_ast(valid_tokens)

    def add_symbol(self, name, addr):
        if name in self.symbols:
            logger.fail("Symbol {0} already declared.", name)
        self.symbols[name[:-1]] = addr

    def append(self, addr, token):
        if addr not in self.nodes:
            self.nodes[addr] = []
        self.nodes[addr].append(token)

    def _generate_ast(self, tokens):
        addr = 0x200
        self.nodes[addr] = []

        for token in tokens:
            if token['class'] == 'T_LABEL':
                self.add_symbol(token['lexeme'], addr)
                continue

            if token['class'] in grammar['T_SOL']:
                self.append(addr, token)
                continue

            if token['class'] == 'T_EOL':
                addr += 0x2  # 8bits > 0x00 - 0xFF
                continue

            try:
                last_token = self.nodes[addr][-1]['class']
                if token['class'] in grammar[last_token]:
                    self.append(addr, token)
                    continue
            except IndexError:
                logger.fail("Syntax Error {0} is invalid instruction in ({1}, {2})",
                            token['lexeme'], token['line'], token['column'])
                continue
            except:
                import ipdb; ipdb.set_trace()

            logger.fail("Syntax Error: {0} {1} is invalid syntax in ({2}, {3})",
                        ' '.join([t['lexeme'] for t in self.nodes[addr]]), token['lexeme'], token['line'], token['column'])
