# -*- coding: utf-8 -*-

from chasm.errors import Logger

logger = Logger()

grammar = {
    'TOKEN_SOL': ['TOKEN_LABEL', 'TOKEN_COMMAND'],
    'TOKEN_LABEL': ['TOKEN_EOL'],
    'TOKEN_COMMAND': ['TOKEN_REGISTER', 'TOKEN_BINARY', 'TOKEN_NIBBLE',
                      'TOKEN_ADDR', 'TOKEN_CONSTANT', 'TOKEN_DELAY',
                      'TOKEN_SOUND', 'TOKEN_FONT', 'TOKEN_REGISTER_I',
                      'TOKEN_BINARY', 'TOKEN_VALUE', 'TOKEN_WORD', 'TOKEN_EOL',
                      'TOKEN_NAME', 'TOKEN_MEMORY_I', 'TOKEN_HIGH_FONT', 'TOKEN_FLAG',
                      'TOKEN_BYTE'],
    'TOKEN_ADDR': ['TOKEN_EOL', 'TOKEN_COMMA'],
    'TOKEN_BYTE': ['TOKEN_EOL'],
    'TOKEN_NIBBLE': ['TOKEN_EOL'],
    'TOKEN_NAME': ['TOKEN_EOL'],
    'TOKEN_CONSTANT': ['TOKEN_EOL'],
    'TOKEN_VALUE': ['TOKEN_EOL'],
    'TOKEN_REGISTER': ['TOKEN_COMMA', 'TOKEN_EOL'],
    'TOKEN_DELAY': ['TOKEN_COMMA', 'TOKEN_EOL'],
    'TOKEN_SOUND': ['TOKEN_COMMA'],
    'TOKEN_BINARY': ['TOKEN_COMMA'],
    'TOKEN_FONT': ['TOKEN_COMMA'],
    'TOKEN_KEYBOARD': ['TOKEN_EOL'],
    'TOKEN_REGISTER_I': ['TOKEN_COMMA'],
    'TOKEN_MEMORY_I': ['TOKEN_COMMA', 'TOKEN_EOL'],
    'TOKEN_HIGH_FONT': ['TOKEN_COMMA'],
    'TOKEN_FLAG': ['TOKEN_COMMA', 'TOKEN_EOL'],
    'TOKEN_COMMA': ['TOKEN_REGISTER', 'TOKEN_BYTE', 'TOKEN_NIBBLE',
                    'TOKEN_DELAY', 'TOKEN_KEYBOARD', 'TOKEN_MEMORY_I',
                    'TOKEN_FLAG', 'TOKEN_ADDR', 'TOKEN_NAME'],
    'TOKEN_EOL': []
}


class Ast(object):

    def __init__(self, tokens):
        self.nodes = {}
        self.symbols = {}
        valid_tokens = filter(lambda token: token['class'] not in ('TOKEN_WHITESPACE', 'TOKEN_COMMENT'), tokens)
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
            if token['class'] == 'TOKEN_LABEL':
                self.add_symbol(token['lexeme'], addr)
                continue

            if token['class'] in grammar['TOKEN_SOL']:
                self.append(addr, token)
                continue

            if token['class'] == 'TOKEN_EOL':
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

            logger.fail("Syntax Error: {0} {1} is invalid syntax in ({2}, {3})",
                        ' '.join([t['lexeme'] for t in self.nodes[addr]]), token['lexeme'], token['line'], token['column'])
