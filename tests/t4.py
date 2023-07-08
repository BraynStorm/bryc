from bryc import bryc

def gen(name, value):
    bryc().emit(f"int {name} = {value};")