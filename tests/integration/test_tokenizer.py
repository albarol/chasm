# -*- coding: utf-8 -*-

import unittest
from chasm import lexical
from tests import helpers

class TokenizerTestCase(unittest.TestCase):

    def test_tokenize_asm(self):

        # Arrange:
        with open(helpers.FIXTURES_PATH + '/pong.asm') as fd:
            code = fd.read()

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertTrue(len(tokens) > 0)

    def test_throws_exception_when_asm_is_invalid(self):

        # Arrange:
        with open(helpers.FIXTURES_PATH + '/invalid_pong.asm') as fd:
            code = fd.read()

        # Act:
        # Assert:
        try:
            lexical.tokenize(code)
        except lexical.UnknowTokenError, e:
            self.assertEqual("Invalid token: LTD", e.message)
