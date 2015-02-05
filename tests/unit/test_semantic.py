# -*- coding: utf-8 -*-

import unittest

from chasm import semantic, lexical, syntactic, errors

logger = errors.Logger()


class SemanticTestCase(unittest.TestCase):

    def setUp(self):
        logger.clear()

    def test_validate_valid_ast_node(self):

        # Arrange:
        node = [{'class': 'T_COMMAND', 'lexeme': 'LD', 'column': 1, 'line': 1},
                {'class': 'T_REGISTER', 'lexeme': 'VA', 'column': 4, 'line': 1},
                {'class': 'T_COMMA', 'lexeme': ',', 'column': 6, 'line': 1},
                {'class': 'T_NUMBER', 'lexeme': '2', 'column': 8, 'line': 1}]

        # Act:
        semantic.check_instruction(node)

        # Arrange:
        self.assertFalse(logger.has_error)

    def test_should_accept_16bit_values_for_dw(self):
        # Arrange:
        node = [{'class': 'T_COMMAND', 'lexeme': 'DW', 'column': 1, 'line': 1},
                {'class': 'T_CONSTANT', 'lexeme': '32896', 'column': 3, 'line': 1}]

        # Act:
        semantic.check_memory_address(node)

        # Arrange:
        self.assertFalse(logger.has_error)

    def test_validate_has_error_ast_node(self):

        # Arrange:
        node = [{'class': 'T_COMMAND', 'lexeme': 'CLS', 'column': 1, 'line': 1},
                {'class': 'T_REGISTER', 'lexeme': 'VA', 'column': 4, 'line': 1},
                {'class': 'T_COMMA', 'lexeme': ',', 'column': 6, 'line': 1},
                {'class': 'T_CONSTANT', 'lexeme': '#02', 'column': 8, 'line': 1}]

        # Act:
        semantic.check_instruction(node)

        # Arrange:
        self.assertTrue(logger.has_error)

    def test_validate_valid_memory(self):

        # Arrange:
        node = [{'class': 'T_COMMAND', 'lexeme': 'LDI', 'column': 1, 'line': 1},
                {'class': 'T_CONSTANT', 'lexeme': '0x2EA', 'column': 8, 'line': 1}]

        # Act:
        semantic.check_memory_address(node)

        # Arrange:
        self.assertFalse(logger.has_error)

    def test_validate_invalid_memory_address(self):

        # Arrange:
        node = [{'class': 'T_COMMAND', 'lexeme': 'JMP', 'column': 1, 'line': 1},
                {'class': 'T_NUMBER', 'lexeme': '4099', 'column': 8, 'line': 1}]

        # Act:
        semantic.check_memory_address(node)

        # Arrange:
        self.assertTrue(logger.has_error)

    def test_analyze_entire_ast(self):

        # Arrange:
        code = "LD VA, #02\nLD VB, #02\n"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)

        # Act:
        # Arrange:
        self.assertTrue(semantic.analyze(ast))

    def test_has_error_analyze_entire_ast(self):

        # Arrange:
        code = "LD VA, Play\nJP 409\n"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)

        # Act:
        semantic.analyze(ast)

        # Arrange:
        self.assertTrue(logger.has_error)

    def test_validate_if_name_exists_in_symbol_table(self):

        # Arrange:
        code = "Play: LD VA, 2\nJP Args\nArgs: DRW V0, V1, 1"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)

        # Act:
        semantic.analyze(ast)

        # Arrange:
        self.assertFalse(logger.has_error)

    def test_throw_exception_when_validate_if_name_does_not_exists_in_symbol_table(self):

        # Arrange:
        code = "Play: LD VA, 2\nJP Draw\nArgs: DRW V0, V1, 1"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)

        # Act:
        semantic.analyze(ast)

        # Arrange:
        self.assertTrue(logger.has_error)
