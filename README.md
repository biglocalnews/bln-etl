# BLN ETL

- [Overview](#overview)
- [Install](#install)
- [Usage](#usage)
  - [API](#api)
  - [Git Repository](#git-repository)
  - [Archive](#archive)

## Overview

Utilities to assist with data gathering for and publishing to [Big Local News][].
It supports common workflows used by the BLN core team for its own data
gathering operations, but may also be useful to others working with our
platform.

In particular, this package provides utility code to:

- Simplify data acquisition from GitHub repos
- Create a Zip archive
- Upload files to a BLN platform project

## Install

* [Install git CLI tools](https://git-scm.com/downloads)
* Install the `bln_etl` package from GitHub:
  ```python
  TK: pip install <github repo url after open sourcing>
  ```
* Sign in to [Big Local News][] and create an API key in `Developer -> Manage Keys`
* Set the `BLN_API_KEY=<YOUR_KEY>` environment variable obtained in prior step

## Usage

### Api

> Below examples assume you've configured the `BLN_API_KEY` environment
> variable.

Get projects.

```python
from bln_etl import Client

# Set up the client
client = Client()

# Get your own projects
client.user_projects

# Get our Open Projects
client.open_projects
```

Get a particular project.

```python
from bln_etl import Project

# Projects can be looked up using an "id".
# (accessible, for example, from Client.user_projects)
Project.get('Uadfas19etc.etc.')
```

Create a project.

```python
# Every project requires a name
project_name = 'Awesome Project'

# Optional  fields:
options = {
  'description': 'A truly awesome project.',
  'contact': 'me@aol.com',
  'is_open': True, # projects are private by default
}
Project.create(name, **options)
```

> TODO: The full list of optional fields are:

### Git Repository

The [Repository][] class is a light wrapper around basic Git command-line
utilities. It is a [context manager][] that:

  - automatically creates the project folder if it doesn't exist
  - switches the current working directory to repository folder before executing git commands
  - restores the working directory to its original state upon exit

As such, you should always instantiate `Repository` using a [with statement][].

```python
from bln_etl import Repository

with Repository('/path/to/data-project-repo') as repo:

  # Check if directory is initialized as a git repo
  repo.initialized

  # Initialize directory as a git repo...
  repo.init()

  # ...or clone a repo to the data-project-repo folder
  repo.clone('git@github.com:biglocalnews/bln-etl.git')

  # Stage all file changes
  repo.add()

  # Commit staged changes (a commit message is required)
  message = "Added some code"
  repo.commit(message)

  # Push changes (default: main branch of remote "origin")
  repo.push()

  # Customize the push
  repo.push(remote="upstream", branch="master")
```

[Repository][] also provides a static method that doesn't require use of a
`with` statement:

```python
# Clone a repo to specified local directory
url = 'git@github.com:biglocalnews/bln-etl.git'
target_dir = '/tmp/etl'
Repository.clone_to_dir(url, target_dir)
```


### Archive

A wrapper class to help with creation of [ZipFiles][].

[ZipFiles]: https://docs.python.org/3/library/zipfile.html#zipfile.ZipFile.getinfo

```python
from bln_etl import Archive

archive = Archive('/tmp/data.zip')

# Add a single file
archive.add('/tmp/data.csv')

# Add all files in directory tree
archive.add_dir('/tmp/folder-with-data')

# Add CSVs in directory tree using glob pattern
archive.add_dir('/tmp/folder-with-data', pattern='**/*.csv')

# Include hidden files in directory tree
archive.add_dir('/tmp/folder-with-data', skip_hidden=False)

# List files in archive
archive.list()
```

> See the [`Archive` class][] for additional usage details.

[`Archive` class]: https://github.com/biglocalnews/bln-etl/blob/1cc80233d79b9ec9d091f8b46fd27510c8b59ec4/bln_etl/archive.py#L8
[Big Local News]: https://biglocalnews.org
[context manager]: https://docs.python.org/3/reference/datamodel.html#context-managers
[repository]: https://github.com/biglocalnews/bln-etl/blob/1491e328025466a33339e861aefc5235c32cefb3/bln_etl/repository.py#L6
[with statement]: https://docs.python.org/3/reference/compound_stmts.html#with

## Contributors

Tests use pytest and vcrpy to record live web interactions. A small number of tests
that hit live web services are marked as `webtest` and require an
additional command-line flag to force their execution.

```python
# Run tests
pytest

# Force running of all tests, including live "webtests"
pytest --webtest
```
