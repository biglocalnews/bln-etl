import os

import pytest

from bln_etl.api import Client, Project
from .conftest import fixture_path

TOKEN=os.environ.get('BLN_API_KEY')


@pytest.fixture(scope='module')
def project_uuid():
    return 'UHJvamVjdDo5ZDQyMzE0NS01OWFhLTQ2N2YtYTZmNy0zMjhiZDI1Yzg3OGI='

@pytest.mark.vcr()
def test_user_projects(project_uuid):
    client = Client(api_token=TOKEN)
    projects = client.user_projects
    # Expected attributes
    project = [p for p in projects if p.name == 'Test Project'][0]
    assert project.id == project_uuid
    assert project.name == 'Test Project'
    assert project.slug == 'test-project-UHJvamVjdDo5ZDQ'
    assert project.description == 'Just testing out some stuff'
    assert project.is_open == False
    # Gross test for presence of email
    assert '@' in project.contact
    assert project.contact_method == 'EMAIL'
    assert project.user_role == 'ADMIN'
    assert project.created_at.startswith('2021')
    assert project.updated_at.startswith('2021')


@pytest.mark.vcr()
def test_open_projects():
    client = Client(api_token=TOKEN)
    projects = client.open_projects
    assert len(projects) ==  37
    for proj in projects:
        assert proj.is_open == True


@pytest.mark.vcr()
def test_project_get(project_uuid):
    project = Project.get(project_uuid, api_token=TOKEN)
    assert project.name == 'Test Project'


@pytest.mark.vcr()
def test_project_get_error(project_uuid):
    project = Project.get(project_uuid[:-2], api_token=TOKEN)
    assert project is None


@pytest.mark.vcr()
def test_project_create():
    meta = {
        'is_open': False ,
        'description': 'This is a test project.',
    }
    project = Project.create('Testing', api_token=TOKEN, meta=meta)
    assert project.name == 'Testing'


@pytest.mark.webtest
def test_project_upload_files():
    # NOTE: This is a live webtest to sidestep headaches
    # related to handling errors raised during the process
    # of generating file upload URIs (KeyError: 'createFileUploadUri')
    kwargs = {
        'is_open': False ,
        'description': 'This is a test project.'
    }
    uuid = 'UHJvamVjdDpmMjg3MTU3YS01ODNlLTQzYjktOTkzZS00NmUxNjZhZWNlNmM='
    project = Project.get(uuid, api_token=TOKEN)
    to_upload = [
        fixture_path('test.csv'),
        fixture_path('test2.csv')
    ]
    project.upload_files(to_upload)
    expected = ['test.csv', 'test2.csv']
    actual = [f.name for f in project.files]
    assert actual == expected


@pytest.mark.vcr()
def test_project_files():
    uuid = 'UHJvamVjdDpmMjg3MTU3YS01ODNlLTQzYjktOTkzZS00NmUxNjZhZWNlNmM='
    project = Project.get(uuid, api_token=TOKEN)
    expected = ['test.csv', 'test2.csv']
    actual = [f.name for f in project.files]
    assert actual == expected


@pytest.mark.webtest
def test_project_file_delete():
    uuid = 'UHJvamVjdDpmMjg3MTU3YS01ODNlLTQzYjktOTkzZS00NmUxNjZhZWNlNmM='
    project = Project.get(uuid, api_token=TOKEN)
    expected = ['test.csv', 'test2.csv', 'test.json']
    to_upload = [
        fixture_path('files/test.json')
    ]
    project.upload_files(to_upload)
    actual = [f.name for f in project.files]
    assert 'test.json' in actual
    for f in project.files:
        if f.name == 'test.json':
            f.delete()
    actual = [f.name for f in project.files]
    assert 'test.json' not in actual
