# -*- coding: utf-8 -*-

import unittest

from chasm import disassembler

class DisassemblerTestCase(unittest.TestCase):

    def test_convert_0xFFF_to_SYS(self):

        # Arrange:
        opcodes = [0x0FFF]

        # Act:
        mnemonics = disassembler.generate(opcodes)

        # Assert:
        self.assertEquals('SYS 0xfff', mnemonics[0])

    def test_convert_0xNNNN_to_DW(self):

        # Arrange:
        opcodes = [0xF000]

        # Act:
        mnemonics = disassembler.generate(opcodes)

        # Assert:
        self.assertEquals('DW 0xf000', mnemonics[0])

    def test_convert_0x00E0_to_CLS(self):

        # Arrange:
        opcodes = [0x00E0]

        # Act:
        mnemonics = disassembler.generate(opcodes)

        # Assert:
        self.assertEquals('CLS', mnemonics[0])

    def test_convert_0x00EE_to_RET(self):

        # Arrange:
        opcodes = [0x00EE]

        # Act:
        mnemonics = disassembler.generate(opcodes)

        # Assert:
        self.assertEquals('RET', mnemonics[0])

    def test_convert_0x1FFF_to_JP(self):

        # Arrange:
        opcodes = [0x1FFF]

        # Act:
        mnemonics = disassembler.generate(opcodes)

        # Assert:
        self.assertEquals('JP 0xfff', mnemonics[0])

    def test_convert_0x2FFF_to_CALL(self):

        # Arrange:
        opcodes = [0x2FFF]

        # Act:
        mnemonics = disassembler.generate(opcodes)

        # Assert:
        self.assertEquals('CALL 0xfff', mnemonics[0])

    def test_convert_0x2FFF_to_CALL(self):

        # Arrange:
        opcodes = [0x2FFF]

        # Act:
        mnemonics = disassembler.generate(opcodes)

        # Assert:
        self.assertEquals('CALL 0xfff', mnemonics[0])
