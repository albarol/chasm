import unittest

from chasm import semantic, lexical, syntactic, errors

logger = errors.Logger()

class SemanticTestCase(unittest.TestCase):


    def setUp(self):
        logger.clear()

    def test_validate_valid_ast_node(self):

        # Arrange:
        node = [{'type': 'T_COMMAND', 'value': 'LD', 'column': 1, 'line': 1},
               {'type': 'T_REGISTER', 'value': 'VA', 'column': 4, 'line': 1},
               {'type': 'T_COMMA', 'value': ',', 'column': 6, 'line': 1},
               {'type': 'T_BYTE', 'value': '#02', 'column': 8, 'line': 1}]

        # Act:
        # Arrange:
        self.assertTrue(semantic.is_valid_instruction(node))

    def test_validate_invalid_ast_node(self):

        # Arrange:
        node = [{'type': 'T_COMMAND', 'value': 'CLS', 'column': 1, 'line': 1},
               {'type': 'T_REGISTER', 'value': 'VA', 'column': 4, 'line': 1},
               {'type': 'T_COMMA', 'value': ',', 'column': 6, 'line': 1},
               {'type': 'T_BYTE', 'value': '#02', 'column': 8, 'line': 1}]

        # Act:
        semantic.is_valid_instruction(node)

        # Arrange:
        self.assertTrue(logger.invalid)

    def test_validate_valid_memory(self):

        # Arrange:
        node = [{'type': 'T_COMMAND', 'value': 'LDI', 'column': 1, 'line': 1},
               {'type': 'T_ADDR', 'value': '#2EA', 'column': 8, 'line': 1}]

        # Act:
        # Arrange:
        self.assertTrue(semantic.is_valid_memory_address(node))

    def test_validate_invalid_memory(self):

        # Arrange:
        node = [{'type': 'T_COMMAND', 'value': 'JMP', 'column': 1, 'line': 1},
               {'type': 'T_ADDR', 'value': '#199', 'column': 8, 'line': 1}]

        # Act:
        semantic.is_valid_memory_address(node)

        # Arrange:
        self.assertFalse(logger.invalid)


    def test_analyze_entire_ast(self):

        # Arrange:
        code = "LD VA, #02\nLD VB, #02\n"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)

        # Act:
        # Arrange:
        self.assertTrue(semantic.analyze(ast))

    def test_invalid_analyze_entire_ast(self):

        # Arrange:
        code = "LD VA, #02\nJMP #199\n"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)

        # Act:
        semantic.analyze(ast)
        
        # Arrange:
        self.assertFalse(logger.invalid)

