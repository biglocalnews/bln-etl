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
                        updatedAt
                        contactMethod
                        contact
                        description
                        isOpen
                    }
                }
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
