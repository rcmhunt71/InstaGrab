import os
import typing


class ScanFiles:
    def __init__(self, root_directory: str, file_exts_list=None) -> typing.NoReturn:
        """
        Instantiate Disk Scanner object

        :param root_directory: root directory to start scanning from...
        :param file_exts_list: filter (and record) only these file extensions

        """
        self.directory = root_directory
        self.files = []
        self.extensions = file_exts_list or [None]

        # Get a list of the full filespec for all specified file types starting at self.directory
        for file_ext in self.extensions:
            self.files.extend(self.scan(file_ext))

    def scan(self, ext: str = None) -> typing.List[str]:
        """
        Build a list of all (full filespec) files matching the extension. No extension = all files.

        :param ext: file Extension

        :return: List of files (full filespec) matching the extension.
        """
        if ext is not None:
            files = [os.path.abspath(os.path.join(root, f_name)) for
                     root, file_dir, f_list in os.walk(self.directory) for f_name in f_list if f_name.endswith(ext)]
        else:
            files = [os.path.abspath(os.path.join(root, f_name)) for
                     root, file_dir, f_list in os.walk(self.directory) for f_name in f_list]
        return files
