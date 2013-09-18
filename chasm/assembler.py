# -*- coding: utf-8 -*-

import re
import struct

symbols = [
    { 'pattern': r'SYS0x([\d\a-fA-F]{3})', 'opcode': '0NNN' },
    { 'pattern': 'CLS', 'opcode': '00E0'},
    { 'pattern': 'RET', 'opcode': '00EE'},
    { 'pattern': r'JP0x([\d\a-fA-F]{3}),V[\da-fA-F]{1}', 'opcode': 'BNNN' },
    { 'pattern': r'JP0x([\d\a-fA-F]{3})', 'opcode':  '1NNN' },
    { 'pattern': r'CALL0x([\d\a-fA-F]{3})', 'opcode': '2NNN' },
    { 'pattern': r'SEV([\da-fA-F]{1}),0x([\da-fA-F]{2})', 'opcode': '3XNN' },
    { 'pattern': r'SEV([\da-fA-F]{1}),V([\da-fA-F]{1})', 'opcode': '5XY0' },
    { 'pattern': r'SNEV([\da-fA-F]{1}),0x([\da-fA-F]{2})', 'opcode': '4XNN' },
    { 'pattern': r'SNEV([\da-fA-F]{1}),V([\da-fA-F]{1})', 'opcode': '9XY0' },
    { 'pattern': r'ADDV([\da-fA-F]{1}),0x([\da-fA-F]{2})', 'opcode': '7XNN' },
    { 'pattern': r'ADDV([\da-fA-F]{1}),V([\da-fA-F]{1})', 'opcode': '8XY4' },
    { 'pattern': r'ORV([\da-fA-F]{1}),V([\da-fA-F]{1})', 'opcode': '8XY1' },
    { 'pattern': r'ANDV([\da-fA-F]{1}),V([\da-fA-F]{1})', 'opcode': '8XY2' },
    { 'pattern': r'XORV([\da-fA-F]{1}),V([\da-fA-F]{1})', 'opcode': '8XY3' },
    { 'pattern': r'SUBV([\da-fA-F]{1}),V([\da-fA-F]{1})', 'opcode': '8XY5' },
    { 'pattern': r'SHRV([\da-fA-F]{1}),V([\da-fA-F]{1})', 'opcode': '8XY6' },
    { 'pattern': r'SUBNV([\da-fA-F]{1}),V([\da-fA-F]{1})', 'opcode': '8XY7' },
    { 'pattern': r'SHLV([\da-fA-F]{1}),V([\da-fA-F]{1})', 'opcode': '8XYE' },

    { 'pattern': r'RNDV([\da-fA-F]{1}),0x([\da-fA-F]{2})', 'opcode': 'CXNN' },
    { 'pattern': r'DRWV([\da-fA-F]{1}),V([\da-fA-F]{1}),0x([\da-fA-F]{1})', 'opcode': 'DXYN' },
    { 'pattern': r'SKPV([\da-fA-F]{1})', 'opcode': 'EX9E' },
    { 'pattern': r'SKNPV([\da-fA-F]{1})', 'opcode': 'EXA1' },


    { 'pattern': r'LDI,0x([\d\a-fA-F]{3})', 'opcode': 'ANNN' },
    { 'pattern': r'LDV([\da-fA-F]{1}),0x([\da-fA-F]{2})', 'opcode': '6XNN' },
    { 'pattern': r'LDV([\da-fA-F]{1}),V([\da-fA-F]{1})', 'opcode': '8XY0' },
    { 'pattern': r'LDV([\da-fA-F]{1}),DT', 'opcode': 'FX07' },
    { 'pattern': r'LDV([\da-fA-F]{1}),K', 'opcode': 'FX0A' },
    { 'pattern': r'LDDT,V([\da-fA-F]{1})', 'opcode': 'FX15' },
    { 'pattern': r'LDST,V([\da-fA-F]{1})', 'opcode': 'FX18' },
    { 'pattern': r'ADDI,V([\da-fA-F]{1})', 'opcode': 'FX1E' },
    { 'pattern': r'LDF,V([\da-fA-F]{1})', 'opcode': 'FX29' },
    { 'pattern': r'LDB,V([\da-fA-F]{1})', 'opcode': 'FX33' },
    { 'pattern': r'LD\[I\],V([\da-fA-F]{1})', 'opcode': 'FX55' },
    { 'pattern': r'LDV([\da-fA-F]{1}),\[I\]', 'opcode': 'FX65' },
    { 'pattern': r'LDHF,V([\da-fA-F]{1})', 'opcode': 'FX30' },
    { 'pattern': r'LDR,V([\da-fA-F]{1})', 'opcode': 'FX75' },
    { 'pattern': r'LDV([\da-fA-F]{1}),R', 'opcode': 'FX85' },

    { 'pattern': r'DW0x([\da-fA-F]{4})', 'opcode': 'NNNN' },
    { 'pattern': r'DB0x([\da-fA-F]{1})([\da-fA-F]{2})', 'opcode': 'XY' },
    { 'pattern': r'SCD0x([\da-fA-F]{1})', 'opcode': '00CX' },
    { 'pattern': r'SCD', 'opcode': '00FB' },
    { 'pattern': r'SCR', 'opcode': '00FB' },
    { 'pattern': r'SCL', 'opcode': '00FC' },
    { 'pattern': r'EXIT', 'opcode': '00FD' },
    { 'pattern': r'LOW', 'opcode': '00FE' },
    { 'pattern': r'HIGH', 'opcode': '00FF' }
]


variables = [
    {'token': 'NNNN', 'group': 1 },
    {'token':'NNN','group': 1 },
    {'token':'NN','group': 2},
    {'token':'N', 'group': 3},
    {'token':'X', 'group': 1},
    {'token':'Y', 'group': 2}
]


def generate(ast):
    opcodes = []
    for node in ast.nodes:
        instruction = ''.join([i['value'] for i in node])
        for symbol in symbols:
            match = re.match(symbol['pattern'], instruction)
            if match:
                opcodes.append(pack_opcode(symbol, match))
    return opcodes


def pack_opcode(symbol, match):
    opcode = symbol['opcode']
    for variable in variables:
        if variable['token'] in opcode:
            opcode = opcode.replace(variable['token'], match.group(variable['group']))
    return struct.pack('>H', int(opcode, 16))
