#Сделать все возожные кондишены

from classes import printError

def equal(a, b):
    if(a == b):
        return True
    else:
        return False
def notequal(a, b):
    if(a != b):
        return True
    else:
        return False
def more(a, b):
    try:
        a1 = int(a)
        b1 = int(b)
    except Exception:
        printError("Wrong condition")
        return
    if(a1 > b1):
        return True
    else:
        return False
def less(a, b):
    try:
        a1 = int(a)
        b1 = int(b)
    except Exception:
        printError("Wrong condition")
        return
    if(a1 < b1):
        return True
    else:
        return False
def moreorequal(a, b):
    try:
        a1 = int(a)
        b1 = int(b)
    except Exception:
        printError("Wrong condition")
        return
    if(a1 >= b1):
        return True
    else:
        return False
def lessorequal(a, b):
    try:
        a1 = int(a)
        b1 = int(b)
    except Exception:
        printError("Wrong condition")
        return
    if(a1 <= b1):
        return True
    else:
        return False