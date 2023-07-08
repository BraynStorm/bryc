from bryc import bryc


def create_variable(
    name: str,
    type: str,
    value: object | None = None,
    array: int | list[int] = -1,
    static: bool = False,
    inline: bool = False,
    extern: bool = False,
    const: bool = False,
):
    p = ""
    if extern:
        p += "extern "
    if static:
        p += "static "
    if inline:
        p += "inline "
    if const:
        c = " const"
    else:
        c = ""

    if value is None:
        maybe_value = ""
    else:
        maybe_value = f" = {value}"

    if array == -1:
        maybe_array = ""
    elif isinstance(array, int):
        maybe_array = f"[{array}]"
    else:
        maybe_array = "".join(map(lambda a: f"[{a}]", array))
    p += f"{type}{c} {name}{maybe_array}{maybe_value};"

    bryc().emit(p)
