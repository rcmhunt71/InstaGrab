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


class MediaRecord:
    """ Class for storing information about a single media file"""

    def __init__(self, name: str = None, url: str = None, paths: typing.List[str] = None,
                 metadata: typing.Dict[str, typing.Any] = None, db_index: str = DatabaseIndices.UNKNOWN,
                 media_type: MediaTypes = MediaTypes.UNKNOWN) -> typing.NoReturn:
        self.name = name
        self.url = url
        self.paths = paths or []
        self.metadata = metadata or {}
        self.media_type = media_type
        self.db_index = db_index
        if MediaMetadata.FAVORITE not in self.metadata:
            self.metadata[MediaMetadata.FAVORITE] = False

    def __str__(self):
        paths = '\n\t       '.join([f'"{n}"' for n in self.paths])
        return (f"FILENAME: {self.name} {'(FAVORITE)' if MediaMetadata.FAVORITE in self.metadata else ''}\n"
                f"\tTYPE: {self.media_type.value}\n"
                f"\tMETADATA: {self.metadata}\n"
                f"\tPATHS: {paths}\n"
                f"\tURL: {self.url}\n"
                f"\tINDEX: {self.db_index}")
