import shutil
import subprocess
from pathlib import Path

import pytest

from bln_etl import Repository


"""
@pytest.fixture
def create_config(config_path):
    config_fixture = Path(__file__)\
        .parent\
        .joinpath('fixtures/config.yaml')
    shutil.copyfile(config_fixture, config_path)


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv(
        'BLN_API_KEY',
        '3rafaj;adksfh;ac'
    )
"""


@pytest.fixture(scope='module')
def vcr_config():
    return {
        'filter_headers': [('Authorization', 'JWT DUMMY')],
    }

## Helper functions
def fixture_path(file_name):
    return str(
        Path(__file__)\
            .parent\
            .joinpath('fixtures')\
            .joinpath(file_name)
    )


def file_contents(pth):
    with open(pth, 'r') as f:
        return f.read()


def read_fixture(file_name):
    path = str(
        Path(__file__)\
            .parent\
            .joinpath('fixtures')\
            .joinpath(file_name)
    )
    return file_contents(path)


def repo_status():
    return subprocess.check_output(['git', 'status']).decode('utf-8')


def repo_log(num=1):
    return subprocess.check_output(['git', 'log']).decode('utf-8')


# Fixtures
@pytest.fixture
def git_project_dir(tmp_path):
    return str(tmp_path.joinpath('fake-repo'))


@pytest.fixture
def init_repo(git_project_dir):
    with Repository(git_project_dir) as repo:
        repo.init()


@pytest.fixture
def create_readme(git_project_dir):
    readme = Path(git_project_dir).joinpath("README.md")
    content = "Example readme for a test project"
    with open(readme, 'w') as fh:
        fh.write(content)


@pytest.fixture
def stage_files(git_project_dir):
    with Repository(git_project_dir) as repo:
        repo.add()


@pytest.fixture
def working_dir(tmp_path):
    return str(
        tmp_path.joinpath('working_dir')
    )


@pytest.fixture
def create_working_dir(working_dir):
    Path(working_dir).mkdir(parents=True, exist_ok=True)

