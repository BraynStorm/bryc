import argparse
import logging
import os
import sys
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union  # NOTE: Python <3.10 support

logging.basicConfig(
    level=os.environ.get("BRYC_LOGLEVEL", "INFO"),
    # format="%(levelname)01s | %(message)s",
    format="{levelname} | {message}",
    style="{",
)
logger = logging.getLogger(__name__)


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

    def call(self, module_name: str, function: str, *args, **kwargs):
        """
        Equivalent of:
        ```python
            import {module_name}
            value = {module_name}.{function}(*args, **kwargs)
            if value:
                bryc().emit(value)
        ```

        If you all your code is already in an external file
        doing:
        ```c
        /* bryc: start
        from module import *

        my_function()
        */
        /* bryc: end */
        ```
        is laborious and annoying. Instead, use this:

        ```c
        /* bryc: start
        bryc().run("module", "my_function")
        */
        /* bryc: end */
        ```

        """
        from importlib import import_module

        module = import_module(module_name)
        function = getattr(module, function)
        if callable(function):
            value = function(*args, **kwargs)

            if value:
                self.emit(value)
        else:
            self.emit(function)


_bryc: bryc_ = None  # type:ignore


def bryc() -> bryc_:
    return _bryc


if __name__ == "__main__":
    from time import time_ns

    start = time_ns()

    parser = argparse.ArgumentParser("python bryc.py")
    parser.add_argument("files", nargs="+")
    parser.add_argument("--verbose", "-v", action="count", default=0)
    args = parser.parse_args()
    if args.verbose >= 3:
        logger.setLevel("DEBUG")
    if args.verbose >= 2:
        logger.setLevel("INFO")
    elif args.verbose >= 1:
        logger.setLevel("WARNING")
    elif args.verbose >= 0:
        logger.setLevel("ERROR")

    argv = getattr(sys, "orig_argv", sys.argv)  # NOTE: Python <3.10 support.
    logger.debug("bryc: invoked as:" + " ".join(argv))

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

    def bryc_find_invocation(text: str, start: int) -> Optional[Invocation]:
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

    def bryc_find_invocation_code(text: str, invocation: Invocation) -> Optional[Code]:
        i_start = text.find("\n", invocation.start, invocation.end)
        if i_start == -1:
            return None
        i_start += 1
        i_end = text.find(BRYC_CODE_END_LINE, i_start, invocation.end)
        if i_end == -1:
            return None

        code = text[i_start:i_end].strip()

        return Code(i_start, i_end + 2, code)

    def bryc_process(file: Union[Path, str]):
        logger.debug(f"bryc: {file}")
        file = Path(file)
        c_code = file.read_text(encoding="utf-8")
        original_c_code = c_code

        old_py_path = list(sys.path)
        sys.path.append(str(file.parent.absolute()))

        global _bryc

        i = 0
        while True:
            invocation = bryc_find_invocation(c_code, i)
            if invocation is None:
                break
            i = invocation.end

            code = bryc_find_invocation_code(c_code, invocation)
            if code is None:
                continue

            _bryc = bryc_("\n")

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
                _bryc.output = "\n"
                _bryc.output += "".join(
                    map(
                        lambda ex: f"#error BRYC: {ex}\n",
                        traceback.format_exc().strip().split("\n"),
                    )
                )
            c_code = c_code[: code.end] + _bryc.output + c_code[invocation.end :]

            sys.path = old_py_path

        if original_c_code != c_code:
            # NOTE(bozho2):
            #   Something was generated.
            file.write_text(c_code)

    for file in args.files:
        bryc_process(file)

    end = time_ns()
    took = end - start
    logger.info(f"bryc: took {took/1_000_000_000:#1.3f}s for {args.files}")


__all__ = ["bryc"]
