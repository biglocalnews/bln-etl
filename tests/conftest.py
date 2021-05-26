import shutil
from pathlib import Path

import pytest


def fixture_path(file_name):
    return str(
        Path(__file__)\
            .parent\
            .joinpath('fixtures')\
            .joinpath(file_name)
    )


