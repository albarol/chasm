import unittest

from chasm import semantic, lexical, syntactic

class SemanticTestCase(unittest.TestCase):

    def test_validate_valid_ast_node(self):

        # Arrange:
        node = [{'type': 'T_COMMAND', 'value': 'LD', 'column': 1, 'line': 1},
               {'type': 'T_REGISTER', 'value': 'VA', 'column': 4, 'line': 1},
               {'type': 'T_COMMA', 'value': ',', 'column': 6, 'line': 1},
               {'type': 'T_BYTE', 'value': '0x02', 'column': 8, 'line': 1}]

        # Act:
        # Arrange:
        self.assertTrue(semantic.is_valid_instruction(node))

    def test_validate_invalid_ast_node(self):

        # Arrange:
        node = [{'type': 'T_COMMAND', 'value': 'CLS', 'column': 1, 'line': 1},
               {'type': 'T_REGISTER', 'value': 'VA', 'column': 4, 'line': 1},
               {'type': 'T_COMMA', 'value': ',', 'column': 6, 'line': 1},
               {'type': 'T_BYTE', 'value': '0x02', 'column': 8, 'line': 1}]

        # Act:
        # Arrange:
        try:
            semantic.is_valid_instruction(node)
        except semantic.InvalidInstructionError, e:
            self.assertEqual("Invalid instruction: CLS VA , 0x02", e.message)

    def test_validate_valid_memory(self):

        # Arrange:
        node = [{'type': 'T_COMMAND', 'value': 'LDI', 'column': 1, 'line': 1},
               {'type': 'T_ADDR', 'value': '0x2EA', 'column': 8, 'line': 1}]

        # Act:
        # Arrange:
        self.assertTrue(semantic.is_valid_memory_address(node))

    def test_validate_invalid_memory(self):

        # Arrange:
        node = [{'type': 'T_COMMAND', 'value': 'JMP', 'column': 1, 'line': 1},
               {'type': 'T_ADDR', 'value': '0x199', 'column': 8, 'line': 1}]

        # Act:
        # Arrange:
        try:
            semantic.is_valid_memory_address(node)
        except semantic.InvalidMemoryAddressError, e:
            self.assertEqual("Invalid memory address: 0x199", e.message)


    def test_analyze_entire_ast(self):

        # Arrange:
        code = "LD VA, 0x02\nLD VB, 0x02\n"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)

        # Act:
        # Arrange:
        self.assertTrue(semantic.analyze(ast))

    def test_invalid_analyze_entire_ast(self):

        # Arrange:
        code = "LD VA, 0x02\nJMP 0x199\n"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)

        # Act:
        # Arrange:
        try:
            self.assertTrue(semantic.analyze(ast))
        except semantic.InvalidMemoryAddressError, e:
            self.assertEqual("Invalid memory address: 0x199", e.message)
