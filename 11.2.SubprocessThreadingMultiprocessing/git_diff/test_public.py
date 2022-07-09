import zipfile
from dataclasses import dataclass
from pathlib import WindowsPath as Path
import typing as tp

import pytest

from .git_diff import get_changed_dirs


@pytest.fixture(scope="function", autouse=True)
def unzip_git_repo(tmp_path: Path) -> tp.Generator[Path, None, None]:
    with zipfile.ZipFile('C:\\Users\\valee\\anaconda3\\envs\\public-2021-fall-master\\11.2'
                         '.SubprocessThreadingMultiprocessing\\git_diff\\testdata.zip', 'r') as zip_ref:
        zip_ref.extractall(tmp_path)
    yield f'{tmp_path}\\testdata'


tasks = {
    1: 'task1',
    2: 'task2',
    3: 'task3',
    4: 'task4',
    5: 'task5',
    6: 'task6',
    7: 'task7',
}


@dataclass
class Case:
    from_commit_hash: str
    to_commit_hash: str
    expected_dirs: tp.Set[str]


TEST_CASES = [
    Case(
        from_commit_hash='e9bd09aed488b562df0116174ec4feb973e9eb1a',
        to_commit_hash='f8f989433f0d0445070fbee045e93953bce7ba59',
        expected_dirs={tasks[5], tasks[7]}
    ),
    Case(
        from_commit_hash='14356e546a6841cea7132f60c2a5d9bf36dea660',
        to_commit_hash='e9bd09aed488b562df0116174ec4feb973e9eb1a',
        expected_dirs={tasks[3], tasks[6]}
    ),
    Case(
        from_commit_hash='4a9ed009a7e82d6c1c600093c67bea8b990659d3',
        to_commit_hash='ca0a45e88fa9f2b045a5c58636c4041a047ccaf3',
        expected_dirs={tasks[2], tasks[3]}
    ),
    Case(
        from_commit_hash='22ac60faec7b38c68e7a740557e3864dbae1689d',
        to_commit_hash='4a9ed009a7e82d6c1c600093c67bea8b990659d3',
        expected_dirs={tasks[1]}
    ),
]


@pytest.mark.parametrize('case', TEST_CASES, ids=str)
def test_git_diff(case: Case, unzip_git_repo: Path) -> None:
    dirs = get_changed_dirs(
        unzip_git_repo,
        case.from_commit_hash,
        case.to_commit_hash
    )

    assert dirs == {unzip_git_repo / d for d in case.expected_dirs}
