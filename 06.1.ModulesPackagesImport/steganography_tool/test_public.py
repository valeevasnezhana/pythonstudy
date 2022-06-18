import importlib
from importlib import metadata
from pathlib import Path


def test_modules_installed() -> None:
    try:
        import PIL
    except ImportError:
        PIL = None
    assert PIL, 'Can not find `PIL`. It is required?'

    try:
        import steganography_tool
    except ImportError:
        steganography_tool = None  # type: ignore
    assert steganography_tool, 'Can not find `steganography_tool`. It is installed?'


def test_structure() -> None:
    try:
        import steganography_tool
        import steganography_tool.decode
        import steganography_tool.encode
        import steganography_tool.cli
        import steganography_tool.utils  # noqa: F401
    except ImportError as e:
        assert False, f'Please, mind package structure: {e}'


def test_import_module_import() -> None:
    try:
        from steganography_tool import encode_message, decode_message  # noqa: F401
    except ImportError as e:
        assert False, f'Please, mind package structure: {e}'


def test_submodules_wildcard_import() -> None:
    module = importlib.import_module('steganography_tool')
    module_dict = module.__dict__

    assert '__all__' in module_dict, 'You should limit `import *` via __all__'
    assert module_dict['__all__'] == ['encode_message', 'decode_message']


def test_setup_style() -> None:
    task_dir = Path(__file__).resolve().parent

    setup_cfg_file = task_dir / 'setup.cfg'
    assert setup_cfg_file.exists(), 'You should use `setup.cfg`'

    setup_py_file = task_dir / 'setup.py'
    setup_py_n_lines = open(setup_py_file.as_posix()).read().count("\n")
    assert setup_py_n_lines <= 4, 'You should not use `setup.py` in favor of `setup.cfg`'


def test_module_metadata() -> None:
    module_name = 'steganography_tool'
    module_metadata = metadata.metadata(module_name)

    for metadata_field in ['Author', 'Author-email', 'Summary', 'Version']:
        assert module_metadata[metadata_field] and module_metadata[metadata_field] != 'UNKNOWN', \
            f'You should add {metadata_field} in metadata'
