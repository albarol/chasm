
from chasm.errors import Logger

logger = Logger()

grammar = {
    'T_SOL': ['T_LABEL', 'T_COMMAND'],
    'T_LABEL': ['T_EOL'],
    'T_COMMAND': ['T_REGISTER', 'T_BINARY', 'T_NIBBLE',
                  'T_ADDR', 'T_CONSTANT', 'T_DELAY',
                  'T_SOUND', 'T_FONT', 'T_REGISTER_I',
                  'T_BINARY', 'T_VALUE', 'T_WORD', 'T_EOL',
                  'T_NAME', 'T_MEMORY_I', 'T_HIGH_FONT', 'T_FLAG'],
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
                'T_FLAG', 'T_ADDR'],
    'T_EOL': []
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
        valid_tokens = filter(lambda token: token['type'] not in ('T_WHITESPACE', 'T_COMMENT'), tokens)
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

            if token['type'] == 'T_LABEL':
                self.__table.append(token['value'], addr)
            elif not node.tree and token['type'] in grammar['T_SOL']:
                node.append(token)
            elif token['type'] == 'T_EOL':
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


        # append when T_EOL does not exists
        if node.tree:
            self.__nodes.append(node)
