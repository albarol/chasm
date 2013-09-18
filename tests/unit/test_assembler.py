# -*- coding: utf-8 -*-

import unittest
import struct
from chasm import assembler, lexical, syntactic, semantic


class AssemblerTestCase(unittest.TestCase):

    def pack(self, opcode):
        return struct.pack('>H', int('0x%s' % (opcode,), 16))

    def test_convert_SYS_node_to_opcode(self):

        # Arrange:
        code = "SYS 0xfff"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('0FFF'), opcodes[0])

    def test_convert_CLS_node_to_opcode(self):

        # Arrange:
        code = "CLS"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('00E0'), opcodes[0])

    def test_convert_RET_node_to_opcode(self):

        # Arrange:
        code = "RET"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('00EE'), opcodes[0])

    def test_convert_JMP_1NNN_node_to_opcode(self):

        # Arrange:
        code = "JP 0xFFF"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('1FFF'), opcodes[0])

    def test_convert_JMP_BNNN_node_to_opcode(self):

        # Arrange:
        code = "JP 0xFFF, V0"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('BFFF'), opcodes[0])

    def test_convert_CALL_node_to_opcode(self):

        # Arrange:
        code = "CALL 0xFFF"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('2FFF'), opcodes[0])

    def test_convert_SE_3XNN_node_to_opcode(self):

        # Arrange:
        code = "SE V0, 0xFF"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('30FF'), opcodes[0])

    def test_convert_SE_5XY0_node_to_opcode(self):

        # Arrange:
        code = "SE V0, V1"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('5010'), opcodes[0])

    def test_convert_SNE_4XNN_node_to_opcode(self):

        # Arrange:
        code = "SNE V0, 0xae"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('40AE'), opcodes[0])

    def test_convert_SNE_9XY0_node_to_opcode(self):

        # Arrange:
        code = "SNE V1, V5"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('9150'), opcodes[0])

    def test_convert_ADD_7XNN_node_to_opcode(self):

        # Arrange:
        code = "ADD V2, 0xFF"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('72FF'), opcodes[0])

    def test_convert_ADD_8XY4_node_to_opcode(self):

        # Arrange:
        code = "ADD V2, V6"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('8264'), opcodes[0])

    def test_convert_OR_node_to_opcode(self):

        # Arrange:
        code = "OR V2, V6"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('8261'), opcodes[0])

    def test_convert_AND_node_to_opcode(self):

        # Arrange:
        code = "AND V2, V6"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('8262'), opcodes[0])

    def test_convert_XOR_node_to_opcode(self):

        # Arrange:
        code = "XOR V2, V6"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('8263'), opcodes[0])

    def test_convert_SUB_node_to_opcode(self):

        # Arrange:
        code = "SUB V3, V4"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('8345'), opcodes[0])

    def test_convert_SHR_node_to_opcode(self):

        # Arrange:
        code = "SHR V3, V4"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('8346'), opcodes[0])

    def test_convert_SUBN_node_to_opcode(self):

        # Arrange:
        code = "SUBN V3, V4"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('8347'), opcodes[0])

    def test_convert_SHL_node_to_opcode(self):

        # Arrange:
        code = "SHL V3, V4"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('834E'), opcodes[0])

    def test_convert_LDI_node_to_opcode(self):

        # Arrange:
        code = "LD I, 0xffe"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('AFFE'), opcodes[0])

    def test_convert_RND_node_to_opcode(self):

        # Arrange:
        code = "RND V1, 0xFF"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('C1FF'), opcodes[0])

    def test_convert_DRW_node_to_opcode(self):

        # Arrange:
        code = "DRW V1, V9, 0xF"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('D19F'), opcodes[0])

    def test_convert_SKP_node_to_opcode(self):

        # Arrange:
        code = "SKP V0"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('E09E'), opcodes[0])

    def test_convert_SKNP_node_to_opcode(self):

        # Arrange:
        code = "SKNP V0"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('E0A1'), opcodes[0])

    def test_convert_LDI_FX55_node_to_opcode(self):

        # Arrange:
        code = "LD [I], V1"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('F155'), opcodes[0])

    def test_convert_FILL_node_to_opcode(self):

        # Arrange:
        code = "LD V1, [I]"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('F165'), opcodes[0])

    def test_convert_LD_6XNN_node_to_opcode(self):

        # Arrange:
        code = "LD V0, 0xFF"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('60FF'), opcodes[0])

    def test_convert_LD_8XY0_node_to_opcode(self):

        # Arrange:
        code = "LD V0, V2"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('8020'), opcodes[0])

    def test_convert_LD_FX07_node_to_opcode(self):

        # Arrange:
        code = "LD V1, DT"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('F107'), opcodes[0])

    def test_convert_LD_FX0A_node_to_opcode(self):

        # Arrange:
        code = "LD V2, K"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('F20A'), opcodes[0])

    def test_convert_LD_FX15_node_to_opcode(self):

        # Arrange:
        code = "LD DT, V0"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('F015'), opcodes[0])

    def test_convert_LD_FX18_node_to_opcode(self):

        # Arrange:
        code = "LD ST, V3"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('F318'), opcodes[0])

    def test_convert_LD_FX1E_node_to_opcode(self):

        # Arrange:
        code = "ADD I, V4"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('F41E'), opcodes[0])

    def test_convert_LD_FX29_node_to_opcode(self):

        # Arrange:
        code = "LD F, V5"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('F529'), opcodes[0])

    def test_convert_LD_FX33_node_to_opcode(self):

        # Arrange:
        code = "LD B, V6"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('F633'), opcodes[0])

    def test_convert_DW_to_opcode(self):

        # Arrange:
        code = "DW 0xF000"
        tokens = lexical.tokenize(code)
        ast = syntactic.Ast(tokens)
        semantic.analyze(ast)

        # Act:
        opcodes = assembler.generate(ast)

        # Arrange:
        self.assertEqual(self.pack('F000'), opcodes[0])
