import os

from pathlib import Path
from zipfile import ZipFile


class Archive:

    def __init__(self, path):
        self.path = Path(path)

    def add(self, path, drop_root=None):
        """Add file to archive.

        By default, adds base name of file.

        Use "drop_root" to preserve nested directory structure starting after
        a specified path component (non-inclusive of specified path).
        """
        with ZipFile(self.path, 'a') as zfile:
            args = [path]
            kwargs = {}
            if drop_root:
                kwargs['arcname'] = self._arcname(path, drop_root)
            else:
                kwargs['arcname'] = Path(path).name
            zfile.write(path, **kwargs)

    def list(self):
        with ZipFile(self.path, 'r') as zfile:
            return zfile.namelist()

    def add_dir(self, folder, pattern='**/*'):
        """Append directory contents to a zipfile

        Preserves nested structure of files within a directory, 
        automatically dropping the directories leading up to 
        and including the specified folder

        """
        root = Path(folder)
        with ZipFile(self.path, mode='a') as zfile:
            for pth in root.glob(pattern):
                if pth.is_dir():
                    continue
                arcname = self._arcname(pth, root)
                zfile.write(pth, arcname=arcname)

    def _arcname(self, file_path, split_on):
        # Remove root folders and leading slash
        return str(file_path)\
                .split(str(split_on))[-1]\
                .lstrip('/')


    """
    def compress(self):
        output_dir, date = os.path.split(self.project_data_dir)
        zipped_file = f"{output_dir}/{self.metadata['slug']}_{date}.zip"
        with ZipFile(zipped_file, 'w') as output:
            self.files.sort(key=lambda x: (x.isupper(), x[0].islower()))
            for file in self.files:
                output.write(file, os.path.basename(file))
        self.files.append(zipped_file)
    """
