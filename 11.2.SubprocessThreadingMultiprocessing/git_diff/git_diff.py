import subprocess
import typing as tp
from pathlib import WindowsPath as Path


def get_changed_dirs(git_path: Path, from_commit_hash: str, to_commit_hash: str) -> tp.Set[Path]:
    """
    Get directories which content was changed between two specified commits
    :param git_path: path to git repo directory
    :param from_commit_hash: hash of commit to do diff from
    :param to_commit_hash: hash of commit to do diff to
    :return: sequence of changed directories between specified commits
    """
    output = subprocess.run(
        f'git diff --no-index --name-only {from_commit_hash} {to_commit_hash}',
        cwd=git_path,
        capture_output=False
    )

    changed_files = output.stdout.decode('utf-8').strip().split('\n')
    print(changed_files)
    changed_dirs = {git_path / Path(f).parent for f in changed_files}

    return changed_dirs
