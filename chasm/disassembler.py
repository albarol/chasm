# -*- coding: utf-8 -*-

import re

tokens = [
    {'pattern': r'(00[eE]0)', 'mnemonic': 'CLS'},
    {'pattern': r'(00[eE]{2})', 'mnemonic': 'RET'},
    {'pattern': r'0([\da-fA-F]{3})', 'mnemonic': 'SYS 0xnnn'},
    {'pattern': r'1([\da-fA-F]{3})', 'mnemonic': 'JP 0xnnn'},
    {'pattern': r'2([\da-fA-F]{3})', 'mnemonic': 'CALL 0xnnn'},
    {'pattern': r'3([\da-fA-F]{1})([\da-fA-F]{2})', 'mnemonic': 'SE Vx, 0xnn'},
    {'pattern': r'4([\da-fA-F]{1})([\da-fA-F]{2})', 'mnemonic': 'SNE Vx, 0xnn'},
    {'pattern': r'5([\da-fA-F]{1})([\da-fA-F]{1})0', 'mnemonic': 'SE Vx, Vy'},
    {'pattern': r'6([\da-fA-F]{1})([\da-fA-F]{2})', 'mnemonic': 'LD Vx, 0xnn'},
    {'pattern': r'7([\da-fA-F]{1})([\da-fA-F]{2})', 'mnemonic': 'ADD Vx, 0xnn'},
    {'pattern': r'8([\da-fA-F]{1})([\da-fA-F]{1})0', 'mnemonic': 'LD Vx, Vy'},
    {'pattern': r'8([\da-fA-F]{1})([\da-fA-F]{1})1', 'mnemonic': 'OR Vx, Vy'},
    {'pattern': r'8([\da-fA-F]{1})([\da-fA-F]{1})2', 'mnemonic': 'AND Vx, Vy'},
    {'pattern': r'8([\da-fA-F]{1})([\da-fA-F]{1})3', 'mnemonic': 'XOR Vx, Vy'},
    {'pattern': r'8([\da-fA-F]{1})([\da-fA-F]{1})4', 'mnemonic': 'ADD Vx, Vy'},
    {'pattern': r'8([\da-fA-F]{1})([\da-fA-F]{1})5', 'mnemonic': 'SUB Vx, Vy'},
    {'pattern': r'8([\da-fA-F]{1})([\da-fA-F]{1})6', 'mnemonic': 'SHR Vx, Vy'},
    {'pattern': r'8([\da-fA-F]{1})([\da-fA-F]{1})7', 'mnemonic': 'SUBN Vx, Vy'},
    {'pattern': r'8([\da-fA-F]{1})([\da-fA-F]{1})[Ee]', 'mnemonic': 'SHL Vx, Vy'},
    {'pattern': r'9([\da-fA-F]{1})([\da-fA-F]{1})0', 'mnemonic': 'SNE Vx, Vy'},
    {'pattern': r'[aA]([\da-fA-F]{3})', 'mnemonic': 'LD I, 0xnnn'},
    {'pattern': r'[bB]([\da-fA-F]{3})', 'mnemonic': 'JP 0xnnn, V0'},
    {'pattern': r'[cC]([\da-fA-F]{1})([\da-fA-F]{2})', 'mnemonic': 'RND Vx, 0xnn'},
    {'pattern': r'[dD]([\da-fA-F]{1})([\da-fA-F]{1})([\da-fA-F]{1})', 'mnemonic': 'DRW Vx, Vy, 0xn'},
    {'pattern': r'[eE]([\da-fA-F]{1})9[Ee]', 'mnemonic': 'SKP Vx'},
    {'pattern': r'[eE]([\da-fA-F]{1})[aA]1', 'mnemonic': 'SKNP Vx'},
    {'pattern': r'[fF]([\da-fA-F]{1})07', 'mnemonic': 'LD Vx, DT'},
    {'pattern': r'[fF]([\da-fA-F]{1})0[aA]', 'mnemonic': 'LD Vx, K'},
    {'pattern': r'[fF]([\da-fA-F]{1})15', 'mnemonic': 'LD DT, Vx'},
    {'pattern': r'[fF]([\da-fA-F]{1})18', 'mnemonic': 'LD ST, Vx'},
    {'pattern': r'[fF]([\da-fA-F]{1})1[Ee]', 'mnemonic': 'ADD I, Vx'},
    {'pattern': r'[fF]([\da-fA-F]{1})29', 'mnemonic': 'LD F, Vx'},
    {'pattern': r'[fF]([\da-fA-F]{1})33', 'mnemonic': 'LD B, Vx'},
    {'pattern': r'[fF]([\da-fA-F]{1})55', 'mnemonic': 'LD [I], Vx'},
    {'pattern': r'[fF]([\da-fA-F]{1})65', 'mnemonic': 'LD Vx, [I]'},
    {'pattern': r'([\da-fA-F]{4})', 'mnemonic': 'DW 0xnnnn'},
]


def generate(opcodes):
    mnemonics = []
    for opcode in opcodes:
        instruction = hex(opcode)[2:].rjust(4, '0')
        for token in tokens:
            match = re.match(token['pattern'], instruction)
            if match:
                mnemonic = token['mnemonic']
                if 'nnnn' in token['mnemonic']:
                    mnemonic = mnemonic.replace('0xnnnn', "#{0}".format(match.group(1)))
                elif 'nnn' in token['mnemonic']:
                    mnemonic = mnemonic.replace('0xnnn', "#{0}".format(match.group(1)))
                elif 'nn' in token['mnemonic']:
                    mnemonic = mnemonic.replace('0xnn', "#{0}".format(match.group(2)))
                elif 'n' in token['mnemonic']:
                    mnemonic = mnemonic.replace('0xn', "#{0}".format(match.group(3)))

                if 'Vx' in token['mnemonic']:
                    mnemonic = mnemonic.replace('Vx', "V{0}".format(match.group(1)))
                if 'Vy' in token['mnemonic']:
                    mnemonic = mnemonic.replace('Vy', "V{0}".format(match.group(2)))
                mnemonics.append(mnemonic)
                break
    return mnemonics
