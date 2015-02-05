# -*- coding: utf-8 -*-


def convert_to_hexstring(value):
    if '#' in value:
        return "0x{0}".format(value[1:])
    return hex(int(value))
