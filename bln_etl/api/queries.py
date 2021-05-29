project_details_fragment = '''
id
name
description
contact
contactMethod
createdAt
updatedAt
isOpen
'''

USER_PROJECTS_QUERY = f'''
query {{
    user {{
       effectiveProjectRoles {{
            edges {{
                node {{
                    role
                    project {{
                        {project_details_fragment}
                    }}
                }}
            }}
        }}
    }}
}}
'''

OPEN_PROJECTS_QUERY = f'''
query {{
    openProjects {{
        edges {{
            node {{
              {project_details_fragment}
            }}
        }}
    }}
}}
'''


PROJECT_QUERY = f'''
query Node($id: ID!) {{
    node(id: $id) {{
        ... on Project {{
              {project_details_fragment}
        }}
    }}
}}
'''


PROJECT_FILES_QUERY = f'''
query Node($id: ID!) {{
    node(id: $id) {{
        ... on Project {{
            {project_details_fragment}
            files {{
              name
            }}
        }}
    }}
}}
'''

DELETE_FILE_QUERY = '''
mutation DeleteFile($input: FileURIInput!) {
    deleteFile(input: $input) {
      ok
      err
      __typename
    }
}
'''
