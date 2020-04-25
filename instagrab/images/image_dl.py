import os
import re
import string
import random
import typing

import requests


# TODO: Document (docstring and inlines) + typing

class GetMedia:
    IMAGE_NAME_PATTERN = re.compile(r'.*/(?P<image_name>.*(jpg|mp4))', re.IGNORECASE)
    DEFAULT_NAME_LENGTH = 15
    DEFAULT_DIR = ""

    def __init__(self, url_str: str, relative_dir: str = None, index=-1) -> typing.NoReturn:
        self.url = url_str
        self.media_dir = relative_dir or self.DEFAULT_DIR
        self.name = self.get_media_file_name()
        self.index = index

    def set_index(self, index: int):
        self.index = index

    def get_media_file_name(self) -> str:
        """
        Parse the provided URL for an image

        :return: Name of the media file
        """
        match = self.IMAGE_NAME_PATTERN.match(self.url)
        return match.group('image_name') if match else ''.join(
            random.choice(string.ascii_lowercase) for _ in range(self.DEFAULT_NAME_LENGTH))

    def get_full_media_path(self, rel_media_dir=None) -> str:
        """
        Create full relative filespec for image (assumes DEFAULT DIR exists)

        :param rel_media_dir: Relative directory to save files

        :return: Full file spec (<path>/<filename>.<ext>)
        """
        rel_media_dir = rel_media_dir or self.media_dir
        return os.path.sep.join([rel_media_dir, self.get_media_file_name()])

    def download_media(self) -> typing.NoReturn:
        """
        Download the media and write to a binary file.

        :return: None

        """
        target_file = self.get_full_media_path()
        response = requests.get(self.url, stream=True)
        with open(target_file, 'wb') as BIN:
            for characters in response:
                BIN.write(characters)
        if self.index > -1:
            print(f"{self.index}) ", end='')
        print(f"Wrote: {target_file}")
