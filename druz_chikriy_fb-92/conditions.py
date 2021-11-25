# Сделать все возожные кондишены

from classes import printError


def equal(a, b):
    if a == b:
        return True
    else:
        return False


def notequal(a, b):
    if a != b:
        return True
    else:
        return False


def more(a, b):
    if a > b:
        return True
    else:
        return False


def less(a, b):
    if a < b:
        return True
    else:
        return False


def moreorequal(a, b):
    if a >= b:
        return True
    else:
        return False


def lessorequal(a, b):
    if a <= b:
        return True
    else:
        return False
