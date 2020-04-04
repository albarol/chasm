# -*- coding: utf-8 -*-

import argparse

from chasm import errors, lexical, semantic, assembler, syntactic, disassembler


logger = errors.Logger()


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog='chasm',
        description='Chip8 Assembler',
        epilog=''
    )

    subparsers = parser.add_subparsers(
        title='subcommands',
        description='utilities',
        required=True
    )

    compile_cmd = subparsers.add_parser('compile')
    compile_cmd.add_argument('-i',
        dest="filename", required=True, help='asm file',
        type=argparse.FileType('r')
    )
    compile_cmd.add_argument('-o',
        dest="output", help='c8 file', required=True,
        type=argparse.FileType('wb')
    )
    compile_cmd.set_defaults(func=exec_compile)

    decompile_cmd = subparsers.add_parser('decompile')
    decompile_cmd.add_argument('-i',
        dest="filename", required=True, help='c8 file',
        type=argparse.FileType('rb')
    )
    decompile_cmd.add_argument('-o',
        dest="output", help='asm file', required=True,
        type=argparse.FileType('w+')
    )
    decompile_cmd.set_defaults(func=exec_decompile)

    try:
        args = parser.parse_args(argv[1:] or ['-h'])
        args.func(args)
    except TypeError:
        parser.print_help()


def exec_compile(args):
    import sys

    code = args.filename.read()
    tokens = lexical.tokenize(code)
    ast = syntactic.Ast(tokens)
    semantic.analyze(ast)

    logger.show()
    if logger.has_error:
        sys.exit(-1)

    opcodes = assembler.generate(ast)

    for opcode in opcodes:
        args.output.write(opcode)
    args.output.close()


def exec_decompile(args):
    import array

    opcodes = array.array('H')
    try:
        opcodes.fromfile(args.filename, 1024)
    except EOFError:
        pass

    opcodes.byteswap()
    mnemonics = disassembler.generate(opcodes)
    args.output.write('\n'.join(mnemonics))
    args.output.close()
