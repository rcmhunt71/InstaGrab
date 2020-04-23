from enum import Enum
import os
import pprint
import typing

from instagrab.config.cfg import InstaCfg
from instagrab.config.config_const import ConfigConstants
from instagrab.images.record_file import MediaRecords


class MediaTypes(Enum):
    VIDEO: str = "video"
    AUDIO: str = "audio"
    IMAGE: str = "image"
    UNKNOWN: str = "unknown"


class MediaRecord:
    """ Class for storing information about a single media file"""

    def __init__(self, name: str = None, url: str = None, paths: typing.List[str] = None, favorite: bool = False,
                 media_type: MediaTypes = MediaTypes.UNKNOWN):
        self.name = name
        self.url = url
        self.paths = paths or []
        self.favorite = favorite
        self.media_type = media_type

    def __str__(self):
        paths = '\n\t       '.join([f'"{n}"' for n in self.paths])
        return (f"FILENAME: {self.name} {'(FAVORITE)' if self.favorite else ''}\n"
                f"\tTYPE: {self.media_type.value}\n"
                f"\tPATHS: {paths}\n"
                f"\tURL: {self.url}\n")


class BuildInventory:
    FAVORITE = 'favorite'
    PATHS = 'paths'
    TYPE = 'type'
    URL = 'url'
    UNKNOWN = 'unknown'

    MEDIA_TYPES = {
        'mp3': MediaTypes.AUDIO,
        'mp4': MediaTypes.VIDEO,
        'jpg': MediaTypes.IMAGE,
        'jpeg': MediaTypes.IMAGE,
        'wav': MediaTypes.AUDIO,
        'video': MediaTypes.VIDEO,
        'audio': MediaTypes.AUDIO,
        'image': MediaTypes.IMAGE,
        UNKNOWN: MediaTypes.UNKNOWN,
    }

    MISSING_PATH = "missing_path"
    MISSING_TYPE = "missing_type"
    MISSING_URL = "missing_url"
    MISSING_RECORD = "missing_record"

    def __init__(self, records: typing.Dict[str, str], known_files: typing.List[str],
                 dl_dir: str, cfg: InstaCfg = None):
        """
        Constructor for building data record

        :param records: Dictionary of filename: URL
        :param known_files: List of files from disk
        :param dl_dir: Download directory
        :param cfg: Additional configuration options (optional)

        """
        self.records_on_file = records
        self.file_specs = known_files
        self.dl_dir = dl_dir
        self.cfg = cfg
        self.inv, self.errors = self.build_inventory()
        self.categories = self.get_categories()

    def _ext_type(self, filename: str) -> MediaTypes:
        """
        Determine the file extension type --> media type
        :param filename: mediua filename
        :return: Enum of media type
        """
        extension = filename.split(".")[-1].lower()
        return self.MEDIA_TYPES[extension] if extension in self.MEDIA_TYPES else self.MEDIA_TYPES[self.UNKNOWN]

    @staticmethod
    def _create_inv_record(name: str = None, url: str = None, paths_list: typing.List[str] = None,
                           favorite: bool = False, media_type: MediaTypes = MediaTypes.UNKNOWN) -> MediaRecord:
        """
        Create blank record (or populate with known info)

        :param name: Name of media file
        :param url: URL for media type
        :param paths_list: file paths on disk
        :param favorite: Is this a favorite?
        :param media_type: MediaType enumeration

        :return: Dictionary of info about medio file

        """
        return MediaRecord(name=name, url=url, paths=paths_list, favorite=favorite, media_type=media_type)

    def _update_record_from_filespec(self, file_spec: str, record: MediaRecord) -> MediaRecord:
        """
        Update the record based on info from the file_spec (favorites, add to path list, etc.)

        :param file_spec: file spec media file on disk
        :param record: inventory record

        :return: Updated record

        """
        # Get list of categories/directories that indicate favorite media files
        favorites = [] if self.cfg is None else (
            self.cfg.config.get(ConfigConstants.CATEGORIES, {}).get(ConfigConstants.FAVORITES, []))

        # If filespec has specific directories in the name, mark it as a favorite.
        if len([f for f in favorites if f in file_spec.lower()]) > 0:
            record.favorite = True
        else:
            record.paths.append(file_spec)

        record.media_type = self._ext_type(file_spec.split(os.path.sep)[-1])

        return record

    def build_inventory(self) -> typing.Tuple[typing.Dict[str, MediaRecord], dict]:
        """
        Build a record (dictionary entry) for storing as a record.

        :return: Dictionary of filename:{dict of attributes}

        """
        inv = dict([(name, self._create_inv_record(name=name, url=url)) for name, url in self.records_on_file.items()])

        for file_spec in self.file_specs:
            filename = file_spec.split(os.path.sep)[-1]
            if filename in inv.keys():
                inv[filename] = self._update_record_from_filespec(file_spec=file_spec, record=inv[filename])

        inv, errors = self._validate_inventory(inventory=inv)

        return inv, errors

    def _validate_inventory(self, inventory: typing.Dict[str, MediaRecord]) -> typing.Tuple[dict, dict]:
        """
        Check the inventory for entries that do not exist on disk, are missing critical entries,
        or on disk but not in the inventory. If on disk, but not in the inventory, add it to the
        inventory.

        :param inventory: Dictionary filename:record data

        :return: Tuple of updated inventory and dictionary of errors.

        """

        # Initialize error tracking structure
        errors = {
            self.MISSING_PATH: [],
            self.MISSING_TYPE: [],
            self.MISSING_URL: [],
            self.MISSING_RECORD: [],
        }

        # Check for file records in file and verify it is on disk (file might have been deleted)
        # If found, remove entry from inventory
        for filename in self.records_on_file.keys():
            if not inventory[filename].paths:
                print(f"*ERROR*:\n\tFile '{filename}' listed in the inventory but not found on disk.")
                del inventory[filename]

        # Check file listing on disk against inventory. If files on disk are not in the inventory, add to the inventory.
        missing = 0
        for file_spec in self.file_specs:
            filename = file_spec.split(os.path.sep)[-1]
            if filename not in inventory.keys():
                missing += 1
                errors[self.MISSING_RECORD].append(filename)
                inventory[filename] = self._create_inv_record(
                    name=filename,
                    paths_list=[file_spec],
                    media_type=self._ext_type(filename),
                )
                inventory[filename] = self._update_record_from_filespec(file_spec=file_spec, record=inventory[filename])

        # Check inventory to for entries that are missing data.
        # Record the file names of records with missing data
        for filename, media_data in inventory.items():
            if not media_data.paths:
                errors[self.MISSING_PATH].append(filename)

            if media_data.media_type == MediaTypes.UNKNOWN:
                errors[self.MISSING_TYPE].append(filename)

            if media_data.url == MediaRecords.UNKNOWN or not media_data.url.startswith("http"):
                errors[self.MISSING_URL].append(filename)

        return inventory, errors

    def get_categories(self) -> typing.Dict[str, str]:
        """
        Parse paths to get list of all categories

        :return: Dictionary key:value = "last dir": "complete path"

        """
        categories = {}
        for f_spec in self.file_specs:
            abs_path = os.path.split(os.path.abspath(f_spec))[0]
            file_path = str(os.path.split(f_spec)[0].split(self.dl_dir)[-1])
            categories[str(file_path.split(os.path.sep)[-1])] = abs_path
        return categories

    def show_records(self, filename: str = None, media_type: str = None,
                     favorites: bool = None, keyword: str = None) -> typing.NoReturn:
        """
        Show the information for a given record. (if no record is provided, show all records)

        :param filename: Name of media file.
        :param media_type: Type of media to show
        :param favorites: Display favorites/not_favorites (None = All, True=Favorites, False:!Favorites)
        :param keyword: Search path by keyword (character sequence, no wildcards)

        :return: None

        """
        file_names = list(self.inv.keys()) if filename is None else [filename]
        num_recs_shown = 0
        for f_name in file_names:
            if f_name in self.inv:

                # If media_type filter is specified, do not process anything that does not match
                if media_type is not None and self.inv[f_name].media_type != media_type:
                    continue

                # If favorites filter is specified, do not process anything that does not match
                if favorites is not None and self.inv[f_name].favorite != favorites:
                    continue

                # If a keyword is specified and is not found in the path, do not process.
                if (keyword is not None and
                        len([path for path in self.inv[f_name].paths if keyword.lower() in path.lower()]) == 0):
                    continue

                print(str(self.inv[f_name]))
                num_recs_shown += 1

            else:
                print(f"\tERROR: Requested file is not in the inventory: '{f_name}'")

        print(f"Number of Records shown: {num_recs_shown}")

    def show_errors(self, summary: bool = False, details: bool = False):
        """
        Show detected errors. If neither flag is set, lists file names contained in each error.

        :param summary: List counts for each type of error
        :param details: List specific info for each error.

        :return: None

        """
        if summary:
            print("\nSummary of Errors:")
            for error_type, entry_list in self.errors.items():
                print(f"\t{error_type}: {len(entry_list)}")

        elif details:
            print("\nDetailed Report of Errors:")
            print("\tTo be implemented...")

        else:
            print("\nList of Entries for Each Error:")
            pprint.pprint(self.errors)

        # Blank line after displaying the report
        print()
