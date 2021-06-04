import os
from pathlib import Path
import subprocess


class Repository:
    """Repository is light Python wrapper around basic GIT cli commands.

    The class is a context manager that executes commands in a
    local repository's directory.

    It automatically creates a directory for the repo if it does not yet exist.

    USAGE:
        with Repository('/path/to/git-repo') as repo:
            repo.init()
            assert repo.initialized is True
    """

    def __init__(self, local_path):
        self.path = local_path

    def __enter__(self):
        self.original_path = os.getcwd()
        Path(self.path).mkdir(parents=True, exist_ok=True)
        os.chdir(self.path)
        return self

    def __exit__(self, type, value, traceback):
        os.chdir(self.original_path)

    @property
    def initialized(self):
        return os.path.exists('.git')

    @staticmethod
    def clone_to_dir(url, dir):
        return subprocess.check_output(['git', 'clone', url, dir])

    def clone(self, url):
        self.clone_to_dir(url, '.')

    def init(self):
        return subprocess.check_output(['git', 'init'])

    def add(self):
        return subprocess.check_output(['git', 'add', '.'])

    def commit(self, message):
        return subprocess.check_output(['git', 'commit', '-m', message])

    def add_remote(self, repo_url, name='origin'):
        return subprocess.check_output(['git', 'remote', 'add', name, repo_url])

    def push(self, remote='origin', branch='main'):
        return subprocess.check_output(['git', 'push', '-u', remote, branch])

    def pull(self):
        return subprocess.check_output(['git', 'pull'])
