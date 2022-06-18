import sys
import typing as tp


def input_(prompt: tp.Optional[str] = None,
           inp: tp.Optional[tp.IO[str]] = None,
           out: tp.Optional[tp.IO[str]] = None) -> tp.Optional[str]:
    """Read a string from `inp` stream. The trailing newline is stripped.

    The `prompt` string, if given, is printed to `out` stream without a
    trailing newline before reading input.

    If the user hits EOF (*nix: Ctrl-D, Windows: Ctrl-Z+Return), return None.

    `inp` and `out` arguments are optional and should default to `sys.stdin`
    and `sys.stdout` respectively.
    """
    if inp is None:
        inp = sys.stdin
    if out is None:
        out = sys.stdout
    if prompt is None:
        prompt = ''
    out.write(prompt)
    out.flush()
    while True:
        result = inp.readline()[:len(inp.readlines()) - 1]
        if result:
            return result
        else:
            return None
