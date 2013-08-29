
from chasm.errors import Logger

logger = Logger()

grammar = {
    'TOKEN_SOL': ['TOKEN_LABEL', 'TOKEN_COMMAND'],
    'TOKEN_LABEL': ['TOKEN_EOL'],
    'TOKEN_COMMAND': ['TOKEN_REGISTER', 'TOKEN_BINARY', 'TOKEN_NIBBLE',
                  'TOKEN_ADDR', 'TOKEN_CONSTANT', 'TOKEN_DELAY',
                  'TOKEN_SOUND', 'TOKEN_FONT', 'TOKEN_REGISTER_I',
                  'TOKEN_BINARY', 'TOKEN_VALUE', 'TOKEN_WORD', 'TOKEN_EOL',
                  'TOKEN_NAME', 'TOKEN_MEMORY_I', 'TOKEN_HIGH_FONT', 'TOKEN_FLAG'],
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
                'TOKEN_FLAG', 'TOKEN_ADDR'],
    'TOKEN_EOL': []
}


class AstNode(object):

    def __init__(self, addr=0x000):
        self.__tree = []
        self.addr = addr

    def append(self, token):
        self.__tree.append(token)

    @property
    def tree(self):
        return self.__tree

    def __getitem__(self, key):
        return self.__tree[key]


    def __eq__(self, other):
        assert isinstance(other, AstNode)
        return self.tree == other.tree

class SymbolicTable(object):

    def __init__(self):
        self.__names = {}

    def append(self, name, addr):
        if name in self.__names:
            logger.fail("Symbol table contains this name %s" % (name,))
        self.__names[name[:-1]] = addr

    def __getitem__(self, key):
        return self.__names[key]

    def __contains__(self, key):
        return key in self.__names

    def __len__(self):
        return len(self.__names)


class Ast(object):

    def __init__(self, tokens):
        self.__nodes = []
        self.__table = SymbolicTable()
        valid_tokens = filter(lambda token: token['type'] not in ('TOKEN_WHITESPACE', 'TOKEN_COMMENT'), tokens)
        self._generate_ast(valid_tokens)

    @property
    def nodes(self):
        return filter(lambda node: True if node.tree else False, self.__nodes)

    @property
    def table(self):
        return self.__table

    def _generate_ast(self, tokens):
        addr = 0x200
        index = 0
        node = AstNode(addr=addr)

        while index < len(tokens):
            token = tokens[index]

            if token['type'] == 'TOKEN_LABEL':
                self.__table.append(token['value'], addr)
            elif not node.tree and token['type'] in grammar['TOKEN_SOL']:
                node.append(token)
            elif token['type'] == 'TOKEN_EOL':
                self.__nodes.append(node)
                addr += 1
                node = AstNode(addr=addr)
            elif node.tree and token['type'] in grammar[node.tree[-1]['type']]:
                node.tree.append(token)
            else:
                if not node.tree:
                    logger.fail("Syntax Error %s is invalid instruction in (%s, %s)"
                          % (token['value'], token['line'], token['column']))

                logger.fail("Syntax Error %s %s is invalid syntax in (%s, %s)" %
                           (' '.join([t['value'] for t in node.tree]), token['value'], token['line'], token['column']))
            index += 1


        # append when TOKEN_EOL does not exists
        if node.tree:
            self.__nodes.append(node)
