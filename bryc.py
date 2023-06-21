import sys
import traceback

from dataclasses import dataclass
from pathlib import Path


@dataclass
class bryc:
    """"""

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
    comment_start = "/* bryc: start */"
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
    i_start = text.find("/*", invocation.start, invocation.end)
    if i_start == -1:
        return None

    i_start += 2
    i_end = text.find("*/", i_start, invocation.end)
    if i_end == -1:
        return None

    code = text[i_start:i_end].strip()

    return Code(i_start, i_end + 2, code)


emit = None


def process(file: Path | str):
    print(f"bryc: {file}")
    global emit
    file = Path(file)
    c_code = file.read_text()

    output = ""

    def emit(_) -> None:
        nonlocal output
        output += str(_)
        output += "\n"

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
            py_code = compile(
                ("\n" * c_code[: code.start + 2].count("\n")) + code.code,
                str(file),
                "exec",
            )
            exec(py_code)
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


for file in sys.argv[1:]:
    if file != "_":
        process(file)
