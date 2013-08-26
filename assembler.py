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
    parser.add_argument('-o', dest="output", help='c8 file')
    parser.add_argument('-x', '--hex', action='store_true')
    parser.add_argument('-b', '--bin', action='store_true')
    args = parser.parse_args()

    code = args.filename.read()
    tokens = chasm.lexical.tokenize(code)
    ast = chasm.syntactic.Ast(tokens)
    chasm.semantic.analyze(ast)

    if logger.invalid:
        logger.show()
        sys.exit(-1)

    opcodes = chasm.assembler.compile(ast)

    with open(CURRENT_PATH + '/' + args.output, 'wb') as fd:
        fd.write(' '.join(opcodes))
