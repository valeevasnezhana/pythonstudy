import sys
import math
from typing import Any, Optional

PROMPT = '>>> '


def run_calc(context: Optional[dict[str, Any]] = None) -> None:
    """Run interactive calculator session in specified namespace"""
    context = context or {}
    context['__builtins__'] = {}
    while True:
        try:
            code = input(PROMPT)
        except EOFError:
            print()
            break
        else:
            if code:
                print(eval(code, context))


if __name__ == '__main__':
    context1 = {'math': math}
    run_calc(context1)
