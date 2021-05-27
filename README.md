# BLN ETL

- [Overview](#overview)
- [Install](#install)
- [Usage](#usage)
  - [Archive](#archive)

## Overview

Utilities to assist with data gathering for and publishing to [Big Local News][].
It supports common workflows used by the BLN core team for its own data
gathering operations, but may also be useful to others working with our
platform.

In particular, this package helps:

- simplifying acquisition of data from GitHub repos
- preparing data for upload to a BLN platform project
- archiving of files as Zips

## Install

* [Install git CLI tools](https://git-scm.com/downloads)
* Install the `bln_etl` package from GitHub:
  ```python
  TK: pip install <github repo url after open sourcing>
  ```
## Usage

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
