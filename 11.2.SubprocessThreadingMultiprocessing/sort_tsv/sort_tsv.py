import subprocess
from pathlib import WindowsPath as Path
import csv


def python_sort(file_in: Path, file_out: Path) -> None:
    """
    Sort tsv file using python built-in sort
    :param file_in: tsv file to read from
    :param file_out: tsv file to write to
    """
    reader = csv.reader(open(file_in), delimiter='\t')

    with open(file_out, 'w', encoding="ascii") as writer:
        for line in sorted(reader, key=lambda x: (int(x[1]), x[0])):
            print('\t'.join(line), file=writer)



def util_sort(file_in: Path, file_out: Path) -> None:
    """
    Sort tsv file using sort util
    :param file_in: tsv file to read from
    :param file_out: tsv file to write to
    """

    subprocess.run(f'SORT /+5 {file_in} /Output {file_out}')