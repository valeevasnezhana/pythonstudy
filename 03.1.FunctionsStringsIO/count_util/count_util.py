import typing as tp
import string


def count_util(text: str, flags: tp.Optional[str] = None) -> dict[str, int]:
    """
    :param text: text to count entities
    :param flags: flags in command-like format - can be:
        * -m stands for counting characters
        * -l stands for counting lines
        * -L stands for getting length of the longest line
        * -w stands for counting words
    More than one flag can be passed at the same time, for example:
        * "-l -m"
        * "-lLw"
    Ommiting flags or passing empty string is equivalent to "-mlLw"
    :return: mapping from string keys to corresponding counter, where
    keys are selected according to the received flags:
        * "chars" - amount of characters
        * "lines" - amount of lines
        * "longest_line" - the longest line length
        * "words" - amount of words
    """
    result = {}
    default = (flags is None) or (flags == '')
    if default or ('m' in flags):
        result['chars'] = len(text)

    if default or ('l' in flags):
        lines = 0
        if text:
            lines = text.count('\n')
            if text[len(text) - 1] != '\n':
                lines += 1
        result['lines'] = lines

    if default or ('L' in flags):
        longest_line = 0
        line_len = 0
        for symbol in text:
            if symbol != '\n':
                line_len += 1
            else:
                line_len = 0
            longest_line = max(longest_line, line_len)
        result['longest_line'] = longest_line

    if default or ('w' in flags):
        result['words'] = len(text.split())

    return result
