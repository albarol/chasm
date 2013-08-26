import unittest

from chasm import syntactic, lexical, errors

logger = errors.Logger()


class SyntacticTestCase(unittest.TestCase):

    def test_should_generate_simple_ast(self):

        # Arrange:
        code = "LD VA, 0x02\n"
        tokens = lexical.tokenize(code)

        # Act:
        ast = syntactic.Ast(tokens)

        # Assert:
        self.assertTrue(len(ast.nodes) > 0)

    def test_should_group_commands_in_ast(self):

        # Arrange:
        tree = [{'type': 'T_COMMAND', 'value': 'LD', 'column': 1, 'line': 1},
                {'type': 'T_REGISTER', 'value': 'VA', 'column': 4, 'line': 1},
                {'type': 'T_COMMA', 'value': ',', 'column': 6, 'line': 1},
                {'type': 'T_BYTE', 'value': '#02', 'column': 8, 'line': 1}]
        code = "LD VA, #02\n"
        tokens = lexical.tokenize(code)

        # Act:
        ast = syntactic.Ast(tokens)

        # Assert:
        self.assertEquals(tree, ast.nodes[0])

    def test_throws_syntactic_error_when_sequence_is_invalid(self):

        # Arrange:
        code = "LD ,"
        tokens = lexical.tokenize(code)

        # Act:
        syntactic.Ast(tokens)

        # Assert:
        self.assertTrue(logger.invalid)

    def test_throws_syntactic_error_when_initialize_with_invalid_value(self):

        # Arrange:
        code = "V0, V1"
        tokens = lexical.tokenize(code)

        # Act:
        syntactic.Ast(tokens)

        # Assert:
        self.assertTrue(logger.invalid)
