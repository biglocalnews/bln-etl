# BLN ETL

Utilities to assist with data gathering and publishing scripts for Big Local News.

In particular, focused on simplying acquisition of data from GitHub and
preparing data for upload to a BLN platform project and archiving of
compressed files.

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

> See the `Archive` class for additional usage details.
