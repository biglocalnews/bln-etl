# BLN ETL

Utilities to assist with data gathering and publishing to Big Local News.

In particular, helper code in this package focuses on:

- simplying acquisition of data from GitHub repos
- preparing data for upload to a BLN platform project
- archiving of files as Zips

- [Install](#install)
- [Archive](#archive)

## Install

Dependencies:

* [Download and install git](https://git-scm.com/downloads)

```python
TK: pip install <github repo url after open sourcing>
```

## Archive

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
