import sys
import traceback
import os
import logging

from dataclasses import dataclass
from pathlib import Path

logging.basicConfig(
    level=os.environ.get("BRYC_LOGLEVEL", "INFO"),
    encoding="utf-8",
    # format="%(levelname)01s | %(message)s",
    format="{levelname} | {message}",
    style="{",
)
logger = logging.getLogger(__name__)

logger.debug("bryc: invoked as:" + " ".join(sys.orig_argv))

# NOTE(bozho2):
#   Hack sys.modules so codegen libraries can do
#       'from bryc import ...'
#   and it is the same as
#       'from __main__ import ...'
#
#   See tests/t1* for a simple example of where it is useful.
sys.modules[Path(__file__).stem] = sys.modules[__name__]


# NOTE(bozho2):
#   Customization point.

BRYC_BLOCK_START_LINE = "/* bryc: start"
BRYC_CODE_END_LINE = "*/"
BRYC_BLOCK_END_LINE = "/* bryc: end */"


@dataclass
class bryc_:
    output: str = ""

    def emit(self, x):
        self.output += str(x) + "\n"


bryc: bryc_ = None


if __name__ == "__main__":
    from time import time_ns

    start = time_ns()

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
        comment_start = BRYC_BLOCK_START_LINE
        comment_end = BRYC_BLOCK_END_LINE
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
        i_end = text.find(BRYC_CODE_END_LINE, i_start, invocation.end)
        if i_end == -1:
            return None

        code = text[i_start:i_end].strip()

        return Code(i_start, i_end + 2, code)

    def bryc_process(file: Path | str):
        logger.debug(f"bryc: {file}")
        file = Path(file)
        c_code = file.read_text(encoding='utf-8')
        original_c_code = c_code

        old_py_path = list(sys.path)
        sys.path.append(str(file.parent.absolute()))

        global bryc

        i = 0
        while True:
            invocation = bryc_find_invocation(c_code, i)
            if invocation is None:
                break
            i = invocation.end

            code = bryc_find_invocation_code(c_code, invocation)
            if code is None:
                continue

            bryc = bryc_("\n")

            # NOTE(bozho2):
            #   This is here to allow "implicitly imported" bryc.
            #   Basically, for simple scripts this saves 1 line:
            #   `from bryc import bryc`
            defs = {"bryc": bryc}
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
                # NOTE(bozho2):
                #   Output the exception's text as `#error BRYC:` lines
                bryc.output = "\n"
                bryc.output += "".join(
                    map(
                        lambda ex: f"#error BRYC: {ex}\n",
                        traceback.format_exc().strip().split("\n"),
                    )
                )
            c_code = c_code[: code.end] + bryc.output + c_code[invocation.end :]

            sys.path = old_py_path

            if original_c_code != c_code:
                # NOTE(bozho2):
                #   Something was generated.
                file.write_text(c_code)

    for file in sys.argv[1:]:
        bryc_process(file)

    end = time_ns()
    took = end - start
    logger.info(f"bryc: took {took/1_000_000_000:#1.3f}s for {file}")


__all__ = ["bryc"]
