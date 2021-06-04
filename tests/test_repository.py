import os
import re
from unittest import mock

import pytest
from .conftest import repo_status, repo_log

from bln_etl import Repository



def test_clone_to_dir(git_project_dir):
    "should clone to specified directory"
    repo_url = 'git@github.com:biglocalnews/bln-etl.git'
    with mock.patch('bln_etl.repository.subprocess.check_output') as check_output:
        Repository.clone_to_dir(repo_url, git_project_dir)
        check_output.assert_called_once_with(
            ['git', 'clone', repo_url, git_project_dir]
        )

def test_clone(git_project_dir):
    "should clone to project directory"
    repo_url = 'git@github.com:biglocalnews/bln-etl.git'
    with mock.patch('bln_etl.repository.subprocess.check_output') as check_output:
        with Repository(git_project_dir) as repo:
            repo.clone(repo_url)
        check_output.assert_called_once_with(['git', 'clone', repo_url, '.'])

def test_init(git_project_dir):
    with Repository(git_project_dir) as repo:
        repo.init()
        assert '.git' in os.listdir(git_project_dir)
        assert repo.initialized is True

def test_directory_management(git_project_dir):
    current_dir = os.getcwd()
    with Repository(git_project_dir) as repo:
        assert os.getcwd().endswith('fake-repo')
    assert os.getcwd() == current_dir

@pytest.mark.usefixtures('init_repo', 'create_readme')
def test_add_untracked(git_project_dir):
    p = "Untracked files.*?README.md"
    with Repository(git_project_dir) as repo:
        assert re.search(p, repo_status(), re.DOTALL)
        repo.add()
        assert "new file:   README.md" in repo_status()

@pytest.mark.usefixtures(
    'init_repo',
    'create_readme',
    'stage_files'
)
def test_commit(git_project_dir):
    with Repository(git_project_dir) as repo:
        repo.commit("Initial commit")
        assert 'Initial commit' in repo_log()

@pytest.mark.usefixtures('init_repo')
def test_add_remote(git_project_dir):
    repo_url = 'git@github.com:biglocalnews/bln-etl.git'
    with mock.patch('bln_etl.repository.subprocess.check_output') as check_output:
        with Repository(git_project_dir) as repo:
            repo.add_remote(repo_url)
        check_output.assert_called_once_with(['git', 'remote', 'add', 'origin', repo_url])

@pytest.mark.usefixtures(
    'init_repo',
    'create_readme',
    'stage_files'
)
def test_push(git_project_dir):
    repo_url = 'git@github.com:biglocalnews/bln-etl.git'
    patch_target = 'bln_etl.repository.subprocess.check_output'
    with mock.patch(patch_target) as check_output:
        with Repository(git_project_dir) as repo:
            repo.commit('Initial commit')
            repo.push()
            expected_calls = [
                (['git', 'commit', '-m', 'Initial commit'],),
                (['git', 'push', '-u', 'origin', 'main'],)
            ]
            actual_calls = [call[1] for call in check_output.mock_calls]
            assert actual_calls == expected_calls


@pytest.mark.usefixtures(
    'init_repo',
    'create_readme',
)
def test_pull(git_project_dir):
    repo_url = 'git@github.com:biglocalnews/bln-etl.git'
    patch_target = 'bln_etl.repository.subprocess.check_output'
    with mock.patch(patch_target) as check_output:
        with Repository(git_project_dir) as repo:
            repo.commit('Initial commit')
            repo.pull()
            expected_calls = [
                mock.call(['git', 'commit', '-m', 'Initial commit']),
                mock.call(['git', 'pull'])
            ]
            #actual_calls = [call[1] for call in check_output.mock_calls]
            assert check_output.mock_calls == expected_calls

