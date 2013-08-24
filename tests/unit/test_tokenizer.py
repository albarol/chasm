import unittest
from chasm import lexical

class TokenizerTestCase(unittest.TestCase):
    

    def test_tokenize_whitespace(self):

        # Arrange:
        code = "ADD V0, 0xEF"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_WHITESPACE', tokens[1].type)
        self.assertEqual(' ', tokens[1].value)

    def test_tokenize_comma(self):

        # Arrange:
        code = "ADD V0, 0xEF"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_COMMA', tokens[3].type)
        self.assertEqual(',', tokens[3].value)

    def test_tokenize_command(self):

        # Arrange:
        code = "ADD V0, 0xEF"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_COMMAND', tokens[0].type)
        self.assertEqual('ADD', tokens[0].value)

    def test_tokenize_memory(self):

        # Arrange:
        code = "ADD V0, 0xEF"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_MEMORY', tokens[5].type)
        self.assertEqual('0xEF', tokens[5].value)

    def test_tokenize_register(self):

        # Arrange:
        code = "ADD V0, 0xEF"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_REGISTER', tokens[2].type)
        self.assertEqual('V0', tokens[2].value)

    def test_tokenize_constant(self):

        # Arrange:
        code = "ADD V0, #FF"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_CONSTANT', tokens[5].type)
        self.assertEqual('#FF', tokens[5].value)

    def test_tokenize_label(self):

        # Arrange:
        code = "Start:\n    ADD V0, #FF"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_LABEL', tokens[0].type)
        self.assertEqual('Start:', tokens[0].value)

    def test_tokenize_delay_timer(self):

        # Arrange:
        code = "LD V0, DT"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_DELAY', tokens[5].type)

    def test_tokenize_sound_timer(self):

        # Arrange:
        code = "LD ST, V0"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_SOUND', tokens[2].type)

    def test_tokenize_registerI(self):

        # Arrange:
        code = "LD I, V0"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_REGISTER_I', tokens[2].type)

    def test_tokenize_font(self):

        # Arrange:
        code = "LD F, V0"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_FONT', tokens[2].type)

    def test_tokenize_binary(self):

        # Arrange:
        code = "LD B, V0"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('T_BINARY', tokens[2].type)


    def test_throw_exception_when_token_is_invalid(self):

        # Arrange:
        code = "LADD V0, #FF"

        # Assert:
        self.assertRaises(lexical.UnknowTokenError, lexical.tokenize, code)

    def test_throw_exception_show_what_token_is_invalid(self):

        # Arrange:
        code = "LADD V0, #FF"

        # Assert:
        try:
            lexical.tokenize(code)
        except lexical.UnknowTokenError, e:
            self.assertEqual('Token not found: LADD', e.message)
