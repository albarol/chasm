#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys

import chasm


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

logger = chasm.errors.Logger()


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file {arg} does not exist!".format(arg=arg))
    else:
        return open(arg, 'r')  # return an open file handle


def write_file(parser, arg):
    return open(arg, 'wb')  # return an open file handle


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chip8 Assembler')
    parser.add_argument('-i', dest="filename", required=True, help='asm file',
                        type=lambda file: is_valid_file(parser, file))
    parser.add_argument('-o', dest="output", help='c8 file', required=True,
                        type=lambda file: write_file(parser, file))
    args = parser.parse_args()

    code = args.filename.read()
    tokens = chasm.lexical.tokenize(code)
    ast = chasm.syntactic.Ast(tokens)
    chasm.semantic.analyze(ast)

    logger.show()
    if logger.invalid:
        sys.exit(-1)

    opcodes = chasm.assembler.generate(ast)

    for opcode in opcodes:
        args.output.write(opcode)
    args.output.close()
