USER_PROJECTS_QUERY = """
query {
    user {
        effectiveProjectRoles {
            edges {
                node {
                    role
                    project {
                        id
                        name
                        contactMethod
                        contact
                        description
                        isOpen
                        createdAt
                        updatedAt
                    }
                }
            }
        }
    }
}
"""

OPEN_PROJECTS_QUERY = """
query {
    openProjects {
        edges {
            node {
              id
              name
              description
              contact
              contactMethod
              createdAt
              updatedAt
              isOpen
            }
        }
    }
}
"""


PROJECT_FILES_QUERY ="""
query Node($id: ID!) {
    node(id: $id) {
        ... on Project {
            id
            name
            files {
              name
            }
        }
    }
}
"""

DELETE_FILE_QUERY = """
mutation DeleteFile($input: FileURIInput!) {
    deleteFile(input: $input) {
      ok
      err
      __typename
    }
}
"""
