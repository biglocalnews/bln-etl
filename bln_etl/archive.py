import os
import glob

from pathlib import Path
from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED


try:
    import zlib
    COMPRESSION_TYPE=ZIP_DEFLATED
except ImportError:
    COMPRESSION_TYPE=ZIP_STORED


class Archive:

    def __init__(self, path):
        self.path = Path(path)

    def add(self, path, mode='a', rename=None, drop_root=None):
        """Add file to archive.

        By default, this method:

        - runs in append mode
        - adds only the base name of file (i.e. drops nested folder structure)

        Use the "mode" flag to set a different Zipfile.write mode.

        Use "rename" to store the file using an alternative name.

        Use "drop_root" to preserve nested directory structure starting after
        a specified path component (non-inclusive of specified path).
        """
        with ZipFile(self.path, mode) as zfile:
            args = [path]
            kwargs = {
                'compress_type': COMPRESSION_TYPE,
            }
            if drop_root:
                kwargs['arcname'] = self._arcname(path, drop_root)
            else:
                kwargs['arcname'] = Path(path).name
            if rename:
                kwargs['arcname'] = self._rename(kwargs['arcname'], rename)
            zfile.write(path, **kwargs)

    def list(self):
        with ZipFile(self.path, 'r') as zfile:
            return zfile.namelist()

    def add_dir(self, folder, mode='a', pattern='**/*', skip_hidden=True):
        """Append directory contents to a zipfile

        Preserves nested structure of files within a directory, 
        automatically dropping the directories leading up to 
        and including the specified folder.

        Skips hidden files and folders by default.

        """
        root = Path(folder)
        with ZipFile(self.path, mode=mode) as zfile:
            for pth in root.glob(pattern):
                if pth.is_dir():
                    continue
                if skip_hidden and pth.name.startswith('.'):
                    continue
                arcname = self._arcname(pth, root)
                zfile.write(
                    pth,
                    arcname=arcname,
                    compress_type=COMPRESSION_TYPE
                )

    def _arcname(self, file_path, split_on):
        # Remove root folders and leading slash
        return str(file_path)\
                .split(str(split_on))[-1]\
                .lstrip('/')

    def _rename(self, arcname, new_name):
        return str(Path(arcname).with_name(new_name))
