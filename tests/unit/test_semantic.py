# -*- coding: utf-8 -*-

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
        code = "LD VA, 0x02\nJP 0x199\n"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)

        # Act:
        semantic.analyze(ast)

        # Arrange:
        self.assertFalse(logger.invalid)

    def test_validate_if_name_exists_in_symbol_table(self):

        # Arrange:
        code = "Play: LD VA, 0x02\nJP Args\nArgs: DRW V0, V1, 0x1"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)

        # Act:
        semantic.analyze(ast)

        # Arrange:
        self.assertFalse(logger.invalid)

    def test_throw_exception_when_validate_if_name_does_not_exists_in_symbol_table(self):

        # Arrange:
        code = "Play: LD VA, 0x02\nJP Draw\nArgs: DRW V0, V1, 0x1"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)

        # Act:
        semantic.analyze(ast)

        # Arrange:
        self.assertTrue(logger.invalid)
