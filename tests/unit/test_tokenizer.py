import unittest
from chasm import lexical, errors

logger = errors.Logger()

class TokenizerTestCase(unittest.TestCase):

    def tearDown(self):
        logger.clear()

    def tesTOKEN_tokenize_comment(self):

        # Arrange:
        code = "; CHIP8 Assembler\n"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('TOKEN_COMMENT', tokens[0]['type'])
        self.assertEqual('; CHIP8 Assembler', tokens[0]['value'])

        self.assertEqual('TOKEN_EOL', tokens[1]['type'])

    def tesTOKEN_tokenize_whitespace(self):

        # Arrange:
        code = "ADD V0, #EF"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('TOKEN_WHITESPACE', tokens[1]['type'])
        self.assertEqual(' ', tokens[1]['value'])

    def tesTOKEN_tokenize_eol(self):

        # Arrange:
        code = "Start:\n  ADD V0, #EF"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('TOKEN_EOL', tokens[1]['type'])
        self.assertEqual('\n', tokens[1]['value'])

    def tesTOKEN_tokenize_name(self):

        # Arrange:
        code = "JMP Draw"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('TOKEN_NAME', tokens[2]['type'])
        self.assertEqual('Draw', tokens[2]['value'])

    def tesTOKEN_tokenize_comma(self):

        # Arrange:
        code = "ADD V0, #EF"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('TOKEN_COMMA', tokens[3]['type'])
        self.assertEqual(',', tokens[3]['value'])

    def tesTOKEN_tokenize_command(self):

        # Arrange:
        code = "ADD V0, #EF"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('TOKEN_COMMAND', tokens[0]['type'])
        self.assertEqual('ADD', tokens[0]['value'])

    def tesTOKEN_tokenize_addr(self):

        # Arrange:
        code = "JMP #FFF"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('TOKEN_ADDR', tokens[2]['type'])
        self.assertEqual('#FFF', tokens[2]['value'])

    def tesTOKEN_tokenize_byte(self):

        # Arrange:
        code = "ADD V0, #EF"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('TOKEN_BYTE', tokens[5]['type'])
        self.assertEqual('#EF', tokens[5]['value'])

    def tesTOKEN_tokenize_nibble(self):

        # Arrange:
        code = "DRW V0, V1, #F"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('TOKEN_NIBBLE', tokens[8]['type'])
        self.assertEqual('#F', tokens[8]['value'])


    def tesTOKEN_tokenize_register(self):

        # Arrange:
        code = "ADD V0, #EF"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('TOKEN_REGISTER', tokens[2]['type'])
        self.assertEqual('V0', tokens[2]['value'])

    def tesTOKEN_tokenize_label(self):

        # Arrange:
        code = "Start:\n    ADD V0, #FF"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('TOKEN_LABEL', tokens[0]['type'])
        self.assertEqual('Start:', tokens[0]['value'])

    def tesTOKEN_tokenize_delay_timer(self):

        # Arrange:
        code = "LD V0, DT"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('TOKEN_DELAY', tokens[5]['type'])

    def tesTOKEN_tokenize_sound_timer(self):

        # Arrange:
        code = "LD ST, V0"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('TOKEN_SOUND', tokens[2]['type'])

    def tesTOKEN_tokenize_registerI(self):

        # Arrange:
        code = "LD I, V0"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('TOKEN_REGISTER_I', tokens[2]['type'])

    def tesTOKEN_tokenize_font(self):

        # Arrange:
        code = "LD F, V0"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('TOKEN_FONT', tokens[2]['type'])

    def tesTOKEN_tokenize_keyboard(self):

        # Arrange:
        code = "LD V0, K"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('TOKEN_KEYBOARD', tokens[5]['type'])

    def tesTOKEN_tokenize_binary(self):

        # Arrange:
        code = "LD B, V0"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('TOKEN_BINARY', tokens[2]['type'])

    def tesTOKEN_tokenize_value(self):

        # Arrange:
        code = "LD V1, 2"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual('TOKEN_VALUE', tokens[5]['type'])



    def tesTOKEN_throw_exception_with_invalid_characters(self):

        # Arrange:
        code = "ADD #V0, #FF"

       # Act:
        lexical.tokenize(code)

        # Assert:
        self.assertTrue(logger.invalid)

    def tesTOKEN_show_column_from_asm(self):

        # Arrange:
        code = "ADD V0, #FF\nLD V0, #FE"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual(1, tokens[0]['column'])
        self.assertEqual(5, tokens[2]['column'])
        self.assertEqual(1, tokens[7]['column'])

    def tesTOKEN_show_line_from_asm(self):

        # Arrange:
        code = "ADD V0, #FF\nLD V0, #FE"

        # Act:
        tokens = lexical.tokenize(code)

        # Assert:
        self.assertEqual(1, tokens[0]['line'])
        self.assertEqual(2, tokens[7]['line'])
