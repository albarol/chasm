import re

tokens = [
    { 'pattern': r'(0{4})', 'mnemonic': 'DW #nnnn' },
    { 'pattern': r'(00[eE]0)', 'mnemonic': 'CLS' },
    { 'pattern': r'(00[eE]{2})', 'mnemonic': 'RET' },
    { 'pattern': r'0([\da-fA-F]{3})', 'mnemonic': 'SYS #nnn' },
    { 'pattern': r'1([\da-fA-F]{3})', 'mnemonic': 'JMP #nnn' },
    { 'pattern': r'2([\da-fA-F]{3})', 'mnemonic': 'CALL #nnn' },
    { 'pattern': r'3([\da-fA-F]{1})([\da-fA-F]{2})', 'mnemonic': 'SE Vx, #nn' },
    { 'pattern': r'4([\da-fA-F]{1})([\da-fA-F]{2})', 'mnemonic': 'SNE Vx, #nn' },
    { 'pattern': r'5([\da-fA-F]{1})([\da-fA-F]{1})0', 'mnemonic': 'SE Vx, Vy' },
    { 'pattern': r'6([\da-fA-F]{1})([\da-fA-F]{2})', 'mnemonic': 'LD Vx, #nn' },
    { 'pattern': r'7([\da-fA-F]{1})([\da-fA-F]{2})', 'mnemonic': 'ADD Vx, #nn' },
    { 'pattern': r'8([\da-fA-F]{1})([\da-fA-F]{1})0', 'mnemonic': 'LD Vx, Vy' },
    { 'pattern': r'8([\da-fA-F]{1})([\da-fA-F]{1})1', 'mnemonic': 'OR Vx, Vy' },
    { 'pattern': r'8([\da-fA-F]{1})([\da-fA-F]{1})2', 'mnemonic': 'AND Vx, Vy' },
    { 'pattern': r'8([\da-fA-F]{1})([\da-fA-F]{1})3', 'mnemonic': 'XOR Vx, Vy' },
    { 'pattern': r'8([\da-fA-F]{1})([\da-fA-F]{1})4', 'mnemonic': 'ADD Vx, Vy' },
    { 'pattern': r'8([\da-fA-F]{1})([\da-fA-F]{1})5', 'mnemonic': 'SUB Vx, Vy' },
    { 'pattern': r'8([\da-fA-F]{1})([\da-fA-F]{1})6', 'mnemonic': 'SHR Vx, Vy' },
    { 'pattern': r'8([\da-fA-F]{1})([\da-fA-F]{1})7', 'mnemonic': 'SUBC Vx, Vy' },
    { 'pattern': r'8([\da-fA-F]{1})([\da-fA-F]{1})E', 'mnemonic': 'SHL Vx, Vy' },
    { 'pattern': r'9([\da-fA-F]{1})([\da-fA-F]{1})0', 'mnemonic': 'SNE Vx, Vy' },
    { 'pattern': r'[aA]([\da-fA-F]{3})', 'mnemonic': 'LDI #nnn' },
    { 'pattern': r'[bB]([\da-fA-F]{3})', 'mnemonic': 'JMP #nnn, V0' },
    { 'pattern': r'[cC]([\da-fA-F]{1})([\da-fA-F]{2})', 'mnemonic': 'RND Vx, #nn' },
    { 'pattern': r'[dD]([\da-fA-F]{1})([\da-fA-F]{1})([\da-fA-F]{1})', 'mnemonic': 'DRW Vx, Vy, #n' },
    { 'pattern': r'[eE]([\da-fA-F]{1})9E', 'mnemonic': 'SKP Vx' },
    { 'pattern': r'[eE]([\da-fA-F]{1})A1', 'mnemonic': 'SKNP Vx' },
    { 'pattern': r'[fF]([\da-fA-F]{1})07', 'mnemonic': 'LD Vx, DT' },
    { 'pattern': r'[fF]([\da-fA-F]{1})0A', 'mnemonic': 'LD Vx, K' },
    { 'pattern': r'[fF]([\da-fA-F]{1})15', 'mnemonic': 'LD DT, Vx' },
    { 'pattern': r'[fF]([\da-fA-F]{1})18', 'mnemonic': 'LD ST, Vx' },
    { 'pattern': r'[fF]([\da-fA-F]{1})1E', 'mnemonic': 'LD I, Vx' },
    { 'pattern': r'[fF]([\da-fA-F]{1})29', 'mnemonic': 'LD F, Vx' },
    { 'pattern': r'[fF]([\da-fA-F]{1})33', 'mnemonic': 'LD B, Vx' },
    { 'pattern': r'[fF]([\da-fA-F]{1})55', 'mnemonic': 'STR Vx' },
    { 'pattern': r'[fF]([\da-fA-F]{1})65', 'mnemonic': 'FILL Vx' },
    { 'pattern': r'([\da-fA-F]{4})', 'mnemonic': 'DW #nnnn' },
]

def decompile(opcodes):
    mnemonics = []
    opcodes.byteswap()
    for opcode in opcodes:
        instruction = hex(opcode)[2:].rjust(4, '0')
        for token in tokens:
            match = re.match(token['pattern'], instruction)
            if match:
                mnemonic = token['mnemonic']
                if '#nnnn' in token['mnemonic']:
                    mnemonic = mnemonic.replace('#nnnn', "#%s" % (match.group(1),))
                elif '#nnn' in token['mnemonic']:
                    mnemonic = mnemonic.replace('#nnn', "#%s" % (match.group(1),))
                elif '#nn' in token['mnemonic']:
                    mnemonic = mnemonic.replace('#nn', "#%s" % (match.group(2),))
                elif '#n' in token['mnemonic']:
                    mnemonic = mnemonic.replace('#n', "#%s" % (match.group(3),))

                if 'Vx' in token['mnemonic']:
                    mnemonic = mnemonic.replace('Vx', "V%s" % (match.group(1),))
                if 'Vy' in token['mnemonic']:
                    mnemonic = mnemonic.replace('Vy', "V%s" % (match.group(2),))
                mnemonics.append(mnemonic)
                break
    return mnemonics

