# BLN ETL

- [Overview](#overview)
- [Install](#install)
- [Usage](#usage)
  - [API](#api)
  - [Git Repository](#git-repository)
  - [Archive](#archive)
- [Contributors](#contributors)

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
  ```bash
  pip install git+https://github.com/biglocalnews/bln-etl#egg=bln-etl
  ```
* Sign in to [Big Local News][] and create an API key in `Developer -> Manage Keys`
* Set the `BLN_API_KEY=<YOUR_KEY>` environment variable obtained in prior step

## Usage

### Api

> Below examples assume you've configured the `BLN_API_KEY` environment
> variable. Alternatively, you can pass an `api_token` keyword argument to
> either the `Client` or `Project` classes on instantiation, as well as
> class methods on Project.

Get projects.

```python
from bln_etl.api import Client

# Set up the client
client = Client() # Or Client(api_token=<YOUR_TOKEN>)

# Get your own projects
client.user_projects

# Get our Open Projects
client.open_projects
```

Get a particular project.

```python
from bln_etl.api import Project

# Projects can be looked up using an "id".
# (accessible, for example, from Client.user_projects)
Project.get('Uadfas19etc.etc.')

# Or pass an API token if BLN_API_KEY env var is not set
Project.get('Uadfas19etc.etc.', api_token=<YOUR_TOKEN>)
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

# Or pass an API token if BLN_API_KEY env var is not set
Project.create(name, api_token=<YOUR_TOKEN>)
```
> Below `Project.get` examples assume `BLN_API_KEY` env var is set

Upload files to a project (*silently overwrites pre-existing files of the same name*).

```python
project = Project.get(<uuid>)
to_upload = ['/tmp/test.csv']
project.upload_files(to_upload)
```

List project files.

```python
project = Project.get(<uuid>)
for f in project.files:
    print(f)
```

Delete files.

```python
project = Project.get(<uuid>)
for f in project.files:
    f.delete()
```

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

  # Pull changes (current branch only)
  repo.pull()
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

A wrapper class to help with creation of a [Zipfile][].


```python
from bln_etl import Archive

archive = Archive('/tmp/data.zip')

# Add a single file
archive.add('/tmp/data.csv')

# Add a file but store using a different name
archive.add('/tmp/data.csv', rename='foo.csv')

# Add all files in directory tree
archive.add_dir('/tmp/folder-with-data')

# Add CSVs in directory tree using glob pattern
archive.add_dir('/tmp/folder-with-data', pattern='**/*.csv')

# Include hidden files in directory tree
archive.add_dir('/tmp/folder-with-data', skip_hidden=False)

# Extract files in zip to same dir as zip
archive.extractall()

# Extract files in zip to some other directory
archive.extractall(path="/tmp/some/other/dir")


# List files in archive
archive.list()
```

> See the [`Archive` class][] for additional usage details.

#### Write mode configuration

The `add` and `add_dir` methods operate in *append* mode by default, meaning
they will add files to a new or pre-existing [Zipfile][].

These methods allow you to configure the write mode for Zipfiles.
This can be useful in data scrapers that run on a schedule, allowing you to
use write mode on the first call (thereby deleting a pre-existing Zipfile of the same
name), and then use the default append mode on subsequent calls.

```python
from bln_etl import Archive

archive = Archive('/tmp/data.zip')

# Add a single file using write mode
# to overwrite any previous archive at the same path
archive.add('/tmp/data.csv', mode='w')

# ...or add an entire dir in (over)write mode
archive.add_dir('/tmp/dir-with-lots-of-data', mode='w')

# On subsequent calls, default to append mode 
# to update the new zipfile
archive.add('/tmp/data2.csv')
archive.add_dir('/tmp/some-other-data-dir')
```

#### Compression

The [`Archive` class][] attempts to use Python ZipFile's [ZIP_DEFLATED][] compression type
if the [zlib][] library is installed. If it *is* installed, it uses zlib's
[default compression level][].

If `zlib` or its system-level dependencies are not installed, `Archive` falls back to
ZipFile's default [ZIP_STORED][] compression type (i.e.  uncompressed).


[`Archive` class]: https://github.com/biglocalnews/bln-etl/blob/1cc80233d79b9ec9d091f8b46fd27510c8b59ec4/bln_etl/archive.py#L8
[Big Local News]: https://biglocalnews.org
[context manager]: https://docs.python.org/3/reference/datamodel.html#context-managers
[repository]: https://github.com/biglocalnews/bln-etl/blob/1491e328025466a33339e861aefc5235c32cefb3/bln_etl/repository.py#L6
[with statement]: https://docs.python.org/3/reference/compound_stmts.html#with
[Zipfile]: https://docs.python.org/3/library/zipfile.html#zipfile-objects
[zlib]: https://docs.python.org/3/library/zlib.html
[default compression level]: https://docs.python.org/3/library/zlib.html#zlib.compressobj
[ZIP_DEFLATED]: https://docs.python.org/3/library/zipfile.html#zipfile.ZIP_DEFLATED
[ZIP_STORED]: https://docs.python.org/3/library/zipfile.html#zipfile.ZIP_STORED


## Contributors

Tests use pytest and vcrpy to record live web interactions. A small number of tests
that *always* hit live web services are marked as `webtest` and require an
additional command-line flag to force their execution.

All tests require a valid `BLN_API_KEY` environment variable to be set.
See [Install instructions](#install) for more details.

```python
# Run tests
pytest

# Force running of all tests, including live "webtests"
pytest --webtest
```

To update semantic versioning:

> setup.cfg specifies files to change on version update,
> and is configured to automatically commit and tag file changes

```bash
bumpversion [major|minor|patch]

# e.g., switch 0.1.0 -> 0.1.1
bumpversion patch
```
