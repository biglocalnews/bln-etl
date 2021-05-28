"""Light-weight BLN API wrappers to simplify CRUD
"""
import requests

from bln_etl.api_queries import (
    DELETE_FILE_QUERY,
    PROJECT_FILES_QUERY,
    USER_PROJECTS_QUERY,
)


ENDPOINT = 'https://api.biglocalnews.org/graphql'

class Client:


    def __init__(self, api_token):
        self.api_token = api_token

    @staticmethod
    def post(api_token, data):
        headers = {'Authorization': f'JWT {api_token}'}
        resp = requests.post(
            ENDPOINT,
            json=data,
            headers=headers
        )
        return resp.json()

    @property
    def user_projects(self):
        variables = {}
        data = {
            #"operationName":"effectiveProjectRole",
            'query': USER_PROJECTS_QUERY,
            'variables': variables
        }
        response = self.post(self.api_token, data)
        projects = []
        for edge in response['data']['user']['effectiveProjectRoles']['edges']:
            node = edge['node']
            meta = node['project']
            meta['user_role'] = node['role']
            project = Project(self.api_token, meta)
            projects.append(project)
        return projects

    """
    def open_projects(self, list_files=False):
        response = self.post(self.api_token, {})
    """

class File:

    def __init__(self, api_token, project_id, name):
        self.api_token = api_token
        self.project_id = project_id
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def delete(self):
        variables = {
            "input":{
                "fileName": self.name,
                "projectId":self.project_id,
            }
        }
        data = {
            "operationName":"DeleteFile",
            'query': DELETE_FILE_QUERY,
            'variables': variables
        }
        return Client.post(self.api_token, data)


class Files:

    def __get__(self, obj, owner):
        try:
            return obj._files
        except AttributeError:
            resp = self._get_files(obj)
            obj._files = [
                File(obj.api_token, obj.project.id, node['name'])
                for node in resp['data']['node']['files']
            ]
            return obj._files

    def _get_files(self, obj):
        data = {
            'query': PROJECT_FILES_QUERY,
            'variables': {
                'id': obj.project.id
            }
        }
        return Client.post(obj.api_token, data)


class Project:

    files = Files()

    def __init__(self, api_token=None, attrs={}):
        self.api_token = api_token
        self.attrs = attrs

    def __str__(self):
        return f"<BLN Project: {self.slug}>"

    def __repr__(self):
        return self.__str__()

    @property
    def slug(self):
        slug = self.id[:15]
        try:
            slug += f" - {self.name[:20]}"
            if len(self.name) > 20:
                slug += '...'
        except KeyError:
            pass
        return slug

    @property
    def id(self):
        return self.attrs['id']

    @property
    def name(self):
        return self.attrs['name']

    @property
    def description(self):
        return self.attrs['description']

    @property
    def updated_at(self):
        return self.attrs['updatedAt']

    @property
    def is_open(self):
        return self.attrs['isOpen']

    @property
    def contact(self):
        return self.attrs['contact']

    @property
    def contact_method(self):
        return self.attrs['contactMethod']

    @property
    def user_role(self):
        return self.attrs['user_role']
