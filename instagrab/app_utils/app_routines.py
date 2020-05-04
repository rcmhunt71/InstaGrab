import signal
import typing

import pyperclip

from instagrab.config.cfg import InstaCfg
from instagrab.images.record_file import MediaRecords
from instagrab.images.image_dl import GetMedia
from instagrab.inventory.build_inventory import BuildInventory
from instagrab.inventory.scanner import ScanFiles
from instagrab.images.dl_thread import ThreadedDL
from instagrab.ui.main_window import start_ui


def download_media(record_file: str, flush_records: int = 5, download_dir: str = None) -> typing.NoReturn:
    """
    Read copy buffer, parse URL and download media in URL.

    :param record_file: Name of file to track previous dls and record new dls
    :param flush_records: Number of dl records before writing to file.
    :param download_dir: Relative location of dl directory.

    :return: None

    """

    dl_total = 0        # Current number of DLs during session
    had_dl = False

    # -----------------------------------
    # Catch the Ctrl-C, and write DL'd media names to file.
    # -----------------------------------
    def handler(signal_received: signal.SIGINT, frame: typing.Any):
        print("Control-C captured, exiting.")

        # If there was a file DL'd, write all metadata to file before exiting
        if had_dl:
            names.record_file_names(names_dict)
        exit(0)

    # -----------------------------------
    # Register the interrupt routine
    # -----------------------------------
    signal.signal(signal.SIGINT, handler)

    # -----------------------------------
    # Get list of previously DL'd media names
    #    to save new file info, and prevent duplicate downloads
    # -----------------------------------
    names = MediaRecords(record_file=record_file)
    names_dict = names.get_file_name_dict()

    # -----------------------------------
    # Until CTRL-C is pressed...
    # -----------------------------------
    while True:

        # -----------------------------------
        # Get the URL from the copy buffer
        # -----------------------------------
        url = pyperclip.waitForNewPaste()

        # -----------------------------------
        # Make sure the text from the buffer is an URL
        # -----------------------------------
        if not url.lower().startswith("http"):
            print(f"Invalid URL: {url}")
            continue

        # -----------------------------------
        # Get the media info (url, name, etc.)
        # -----------------------------------
        media = GetMedia(url_str=url, relative_dir=download_dir)

        # -----------------------------------
        # If the media file has not be DL'd, get the media file and
        # record that the media files have been DL'd so name list is written to file.
        # -----------------------------------
        if media.name not in names_dict:
            dl_total += 1
            media.set_index(dl_total)
            names_dict[media.name] = media.url

            # Download the target media from the provided URL
            try:
                media.download_media()

            except Exception as exc:
                names.record_file_names(names_dict)
                print(f"ERROR: {exc}")
                dl_total -= 1

            # Write all of the metadata to file after flush_records DLs
            else:
                had_dl = True
                if dl_total % flush_records == 0:
                    names.record_file_names(names_dict)

        # if the file has the media file name but not the URL, save the URL
        elif names_dict[media.name] == MediaRecords.UNKNOWN:
            names_dict[media.name] = media.url
            print(f"URL updated for {media.name}")

        # -----------------------------------
        # Duplicate media file (it was found in the list), so don't DL the media file.
        # -----------------------------------
        else:
            print(f"NOTE: Media file '{media.name}' has already been downloaded.")


def inventory(records_file: str, download_dir: str = ".", file_ext_list: typing.List[str] = None,
              cfg: InstaCfg = None, debug=False) -> BuildInventory:
    """
    Take an inventory of known media.
    * Media contained in the DL file.
    * Media found on disk (root dir = download_dir)

    :param records_file: File containing all of the DL'd media files.
    :param download_dir: Root dir of where things were DL'd
    :param file_ext_list: File extensions to include in disk inventory
    :param cfg: InstaCfg object (for providing additional configuration options)
    :param debug: Enable debugging

    :return: BuildInventory Object

    """
    file_ext_list = file_ext_list or []

    disks = ScanFiles(root_directory=download_dir, file_exts_list=file_ext_list)
    on_file = MediaRecords(record_file=records_file)
    inv = BuildInventory(records=on_file.get_file_name_dict(), known_files=disks.files, dl_dir=download_dir, cfg=cfg,
                         debug=debug)
    return inv


def query(records_file: str, filename: str = None, keyword: str = None,
          media_type=None, favorites: bool = None, download_dir: str = ".",
          file_ext_list: typing.List[str] = None, cfg: InstaCfg = None, debug=False) -> typing.NoReturn:
    """
    Query the inventory for specific records.

    :param records_file: Name of file storing metadata (optional)
    :param filename: specific file name to query (optional)
    :param keyword: keyword in paths to query (optional)
    :param media_type: type of media to query (optional)
    :param favorites: media that (is/is not) tagged/stored as a favorite (optional)
    :param download_dir: root download directory (optional)
    :param file_ext_list: list of specific file extensions (optional)
    :param cfg: InstaCfg object (for providing additional configuration options)
    :param debug: enable debug logging (optional, default: False)

    NOTE: Need to specify at least one argument for the query to function.

    :return: None

    """

    # Check for a media type
    if media_type is not None:
        if media_type in BuildInventory.MEDIA_TYPES:
            media_type = BuildInventory.MEDIA_TYPES[media_type]
        else:
            print(f"\tERROR: Unrecognized media type: '{media_type}'")
            return

    # Compile query arguments
    args = {'filename': filename, 'media_type': media_type, 'favorites': favorites, 'keyword': keyword}

    if debug:
        import pprint
        print(f"DEBUG: QUERY ARGS: {pprint.pformat(args)}")

    # Get inventory
    inv = inventory(records_file=records_file, download_dir=download_dir, file_ext_list=file_ext_list, cfg=cfg)
    inv.archive_inventory()

    # Filter and display matching inventory based on provided criteria
    inv.show_records(**args)


def ui(records_file: str, dl_engine: ThreadedDL, download_dir: str = ".", cfg: InstaCfg = None, debug=False) -> typing.NoReturn:
    inv = inventory(records_file=records_file, download_dir=download_dir, cfg=cfg, debug=debug)
    inv.archive_inventory()
    start_ui(cfg=cfg, dl_engine=dl_engine)

