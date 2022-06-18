from pathlib import Path
from typing import Union
import pkg_resources  # type: ignore

from PIL import Image
import numpy as np


def read_file(filename: Union[str, Path]) -> np.ndarray:
    with Image.open(filename) as img:
        # width, height = img.size
        data = np.array(img)

    return data


def write_file(data: np.ndarray, filename: Union[str, Path]) -> None:
    new_img = Image.fromarray(data)
    new_img.save(filename)


def get_base_file() -> np.ndarray:
    lenna_filename = pkg_resources.resource_filename(__name__, 'lenna.png')
    return read_file(lenna_filename)
