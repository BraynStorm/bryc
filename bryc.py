import sys
import traceback

from dataclasses import dataclass
from pathlib import Path


@dataclass
class bryc:
    """
    Interpret-time functions.
    """

    @staticmethod
    def emit(x):
        emit(x)


@dataclass
class Range:
    start: int
    end: int


@dataclass
class Invocation(Range):
    pass


@dataclass
class Code(Range):
    code: str


def bryc_find_invocation(text: str, start: int) -> Invocation | None:
    comment_start = "/* # bryc: start"
    comment_end = "/* bryc: end */"
    i_start = text.find(comment_start, start)
    if i_start == -1:
        return None

    i_start += len(comment_start)

    i_end = text.find(comment_end, i_start)
    if i_end == -1:
        return None

    return Invocation(i_start, i_end)


def bryc_find_invocation_code(text: str, invocation: Invocation) -> Code | None:
    i_start = text.find("\n", invocation.start, invocation.end)
    if i_start == -1:
        return None
    i_start += 1
    i_end = text.find("*/", i_start, invocation.end)
    if i_end == -1:
        return None

    code = text[i_start : i_end].strip()

    return Code(i_start, i_end + 2, code)


emit = None


def bryc_process(file: Path | str):
    global emit

    output = ""
    defs = {"bryc": bryc}

    def emit(_) -> None:
        nonlocal output
        output += str(_)
        output += "\n"

    print(f"bryc: {file}")
    file = Path(file)
    c_code = file.read_text()

    i = 0
    while True:
        invocation = bryc_find_invocation(c_code, i)
        if invocation is None:
            break
        i = invocation.end

        code = bryc_find_invocation_code(c_code, invocation)
        if code is None:
            continue

        output = "\n"

        try:
            # NOTE(bozho2):
            #   This ensures the line numbers match if an exception is thrown
            #   and a traceback is displayed.
            extra_lines = "\n" * c_code[: code.start + 2].count("\n")
            py_code = compile(
                extra_lines + code.code,
                str(file),
                "exec",
            )
            exec(py_code, defs, dict(defs))
        except Exception:
            output = "\n"
            output += "".join(
                map(
                    lambda ex: f"#error BRYC: {ex}\n",
                    traceback.format_exc().strip().split("\n"),
                )
            )
        c_code = c_code[: code.end] + output + c_code[invocation.end :]

    file.write_text(c_code)

    emit = None


for file in sys.argv[1:]:
    if file != "_":
        bryc_process(file)
