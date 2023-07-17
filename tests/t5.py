from bryc import bryc


def gen_z():
    bryc().emit("int z = 10;")


def gen_y():
    return "int y = 10;"
