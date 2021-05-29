import os

import pytest

from bln_etl.api import Client, Project


TOKEN=os.environ.get('BLN_API_KEY', 'DUMMY')


@pytest.fixture(scope='module')
def project_uuid():
    return 'UHJvamVjdDo5ZDQyMzE0NS01OWFhLTQ2N2YtYTZmNy0zMjhiZDI1Yzg3OGI='

@pytest.mark.vcr()
def test_user_projects(project_uuid):
    client = Client(TOKEN)
    projects = client.user_projects
    assert len(projects) ==  7
    # Expected attributes
    project = [p for p in projects if p.name == 'Test Project'][0]
    assert project.id == project_uuid
    assert project.name == 'Test Project'
    assert project.slug == 'test-project-UHJvamVjdDo5ZDQ'
    assert project.description == 'Just testing out some stuff'
    assert project.is_open == False
    assert project.contact == 'tumgoren@stanford.edu'
    assert project.contact_method == 'EMAIL'
    assert project.user_role == 'ADMIN'
    assert project.created_at.startswith('2021')
    assert project.updated_at.startswith('2021')


@pytest.mark.vcr()
def test_open_projects():
    client = Client(TOKEN)
    projects = client.open_projects
    assert len(projects) ==  37
    for proj in projects:
        assert proj.is_open == True
