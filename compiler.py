#!/usr/bin/python

import argparse
import os
import sys

import chasm


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

logger = chasm.errors.Logger()


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
       parser.error("The file %s does not exist!"%arg)
    else:
       return open(arg,'r')  #return an open file handle


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chip8 Assembler')
    parser.add_argument('-i', dest="filename", required=True,
                        help='asm file',
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument('-o', dest="output", help='c8 file', required=True)
    args = parser.parse_args()

    code = args.filename.read()
    tokens = chasm.lexical.tokenize(code)
    ast = chasm.syntactic.Ast(tokens)
    chasm.semantic.analyze(ast)

    logger.show()
    if logger.invalid:
        sys.exit(-1)

    opcodes = chasm.assembler.generate(ast)

    with open(CURRENT_PATH + '/' + args.output, 'wb') as fd:
        for  opcode in opcodes:
            fd.write(opcode)
