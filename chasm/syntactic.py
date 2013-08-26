
grammar = {
    'T_SOL': ['T_LABEL', 'T_COMMAND'],
    'T_LABEL': ['T_EOL'],
    'T_COMMAND': ['T_REGISTER', 'T_BINARY', 'T_NIBBLE',
                  'T_ADDR', 'T_CONSTANT', 'T_DELAY',
                  'T_SOUND', 'T_FONT', 'T_REGISTER_I',
                  'T_BINARY', 'T_EOL'],
    'T_ADDR': ['T_EOL', 'T_COMMA'],
    'T_BYTE': ['T_EOL'],
    'T_NIBBLE': ['T_EOL'],
    'T_CONSTANT': ['T_EOL'],
    'T_REGISTER': ['T_COMMA', 'T_EOL'],
    'T_DELAY': ['T_COMMA', 'T_EOL'],
    'T_SOUND': ['T_COMMA'],
    'T_BINARY': ['T_COMMA'],
    'T_FONT': ['T_COMMA'],
    'T_KEYBOARD': ['T_EOL'],
    'T_REGISTER_I': ['T_COMMA'],
    'T_COMMA': ['T_REGISTER', 'T_BYTE', 'T_NIBBLE',
                'T_DELAY', 'T_KEYBOARD'],
    'T_EOL': []
}


class SyntacticError(Exception):
    pass

class Ast(object):

    def __init__(self, tokens):
        self._nodes = []
        valid_tokens = filter(lambda token: token['type'] not in ('T_WHITESPACE', 'T_COMMENT'), tokens)
        self._generate_ast(valid_tokens)

    @property
    def nodes(self):
        return filter(lambda n: True if n else False, self._nodes)

    def _generate_ast(self, tokens):
        index = 0
        command = []

        while index < len(tokens):
            token = tokens[index]
            if not command and token['type'] in grammar['T_SOL']:
                command.append(token)
            elif token['type'] == 'T_EOL':
                self._nodes.append(command)
                command = []
            elif command and token['type'] in grammar[command[-1]['type']]:
                command.append(token)
            else:
                if not command:
                    raise SyntacticError("Syntax Error: %s is invalid instruction in (%s, %s)" 
                          % (token['value'], token['line'], token['column']))
                raise SyntacticError("Syntax Error: %s %s is invalid syntax in (%s, %s)" %
                                  (command[-1]['value'], token['value'], token['line'], token['column']))

            index += 1

        # append when T_EOL does not exists
        if command:
            self._nodes.append(command)
