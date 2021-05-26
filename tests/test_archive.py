from pathlib import Path
from zipfile import ZipFile
from bln_etl.archive import Archive
from .conftest import fixture_path


def test_add_file(tmp_path):
    "should add files, included nested files, as siblings"
    pth = Path(tmp_path, 'archive.zip')
    csv1 = fixture_path('test.csv')
    csv2 = fixture_path('files/test2.csv')
    archive = Archive(pth)
    archive.add(csv1)
    archive.add(csv2)
    files = ZipFile(pth).namelist()
    assert files == ['test.csv', 'test2.csv']

def test_add_file_drop_root(tmp_path):
    "should maintain folder structure relative to specified root"
    pth = Path(tmp_path, 'archive.zip')
    csv3 = fixture_path('files/nested/test3.csv')
    archive = Archive(pth)
    archive.add(csv3, drop_root='files')
    files = ZipFile(pth).namelist()
    assert files == ['nested/test3.csv']

def test_add_nested(tmp_path):
    pth = Path(tmp_path, 'archive.zip')
    infile = fixture_path('test.csv')
    archive = Archive(pth)
    archive.add(infile)
    files = ZipFile(pth).namelist()
    assert files[0].endswith('test.csv')

def test_add_dir(tmp_path):
    pth = Path(tmp_path, 'archive.zip')
    target_dir = fixture_path('files')
    archive = Archive(pth)
    archive.add_dir(target_dir)
    contents = [
        'test.csv',
        'test2.csv',
        'nested/test3.csv'
    ]
    assert ZipFile(pth).namelist() == contents

def test_add_dir_skip_hidden(tmp_path):
    "Should skip hidden files and folders by default"
    pth = Path(tmp_path, 'archive.zip')
    target_dir = fixture_path('files')
    archive = Archive(pth)
    archive.add_dir(target_dir)
    files = ZipFile(pth).namelist()
    assert 'hidden/.secret.txt' not in files

def test_add_dir_include_hidden(tmp_path):
    "Should include hidden files when requested"
    pth = Path(tmp_path, 'archive.zip')
    target_dir = fixture_path('files')
    archive = Archive(pth)
    archive.add_dir(target_dir, skip_hidden=False)
    files = ZipFile(pth).namelist()
    assert '.hidden/.secret.txt' in files

def test_list(tmp_path):
    zip_path = fixture_path('test.zip')
    archive = Archive(zip_path)
    contents = ['test.csv', 'test2.csv']
    assert archive.list() == contents
