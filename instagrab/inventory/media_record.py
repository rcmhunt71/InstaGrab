import datetime
from enum import Enum
import typing

from instagrab.inventory.db_indices import DatabaseIndices


class MediaMetadata:
    GROUP = 'group'
    CATEGORY = 'category'
    FAVORITE = 'favorite'


class MediaTypes(Enum):
    VIDEO: str = "video"
    AUDIO: str = "audio"
    IMAGE: str = "image"
    UNKNOWN: str = "unknown"

    @classmethod
    def get_media_type_enum(cls, media_type):
        for _type in [cls.VIDEO, cls.AUDIO, cls.IMAGE]:
            if _type.value.lower() == media_type:
                return _type
        else:
            return cls.UNKNOWN


class MediaRecord:
    """ Class for storing information about a single media file"""

    def __init__(self, media_file_name: str = None, url: str = None, paths: typing.List[str] = None,
                 metadata: typing.Dict[str, typing.Any] = None, db_index: str = DatabaseIndices.UNKNOWN,
                 media_type: MediaTypes = MediaTypes.UNKNOWN, name: str = None, created=None, modified=None,
                 image_data=None) -> typing.NoReturn:
        self.name = name
        self.media_file_name = media_file_name
        self.url = url
        self.paths = paths or []
        self.metadata = metadata or {}
        self.media_type = media_type
        self.db_index = db_index
        self.image_data = image_data
        self.created = created or datetime.datetime.now()
        self.modified = modified or datetime.datetime.now()
        if MediaMetadata.FAVORITE not in self.metadata:
            self.metadata[MediaMetadata.FAVORITE] = False
        if MediaMetadata.CATEGORY not in self.metadata:
            self.metadata[MediaMetadata.CATEGORY] = None

    def __str__(self):
        paths = '\n\t       '.join([f'"{n}"' for n in set(self.paths)])
        return (f"FILENAME: {self.media_file_name} {'(FAVORITE)' if self.metadata[MediaMetadata.FAVORITE] else ''}\n"
                f"\tCOMMON NAME: {self.name}\n"
                f"\tTYPE: {self.media_type.value}\n"
                f"\tADDED: {self.created}\n"
                f"\tLAST MODIFIED: {self.modified}\n"
                f"\tMETADATA: {self.metadata}\n"
                f"\tPATHS: {paths}\n"
                f"\tURL: {self.url}\n"
                f"\tDB INDEX: {self.db_index}")

    @property
    def favorite(self):
        return self.metadata[MediaMetadata.FAVORITE] if MediaMetadata.FAVORITE in self.metadata else False
