import os

import pytest

from bln_etl.api import Client, Project


TOKEN=os.environ.get('BLN_API_KEY', 'DUMMY')


@pytest.mark.vcr()
def test_user_projects():
    client = Client(TOKEN)
    projects = client.user_projects
    assert len(projects) ==  7
    # Expected attributes
    project = [p for p in projects if p.name == 'Test Project'][0]
    assert project.id.startswith('UHJvamVjdDo5ZDQyMzE0NS0')
    assert project.name == 'Test Project'
    assert project.slug == 'UHJvamVjdDo5ZDQ - Test Project'
    assert project.description == 'Just testing out some stuff'
    assert project.updated_at == '2021-05-21T16:25:23.827000+00:00'
    assert project.is_open == False
    assert project.contact == 'tumgoren@stanford.edu'
    assert project.contact_method == 'EMAIL'
    assert project.user_role == 'ADMIN'


#TODO: open_projects
