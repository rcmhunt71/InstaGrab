import argparse

from instagrab.config.cfg import InstaCfg
from instagrab.config.config_const import ConfigConstants
from instagrab.inventory.build_inventory import BuildInventory


# Bare minimum defaults
default_cfg = "instagrab.yml"
default_records_file = "media_records.txt"
default_download_dir = '.'

# Read configuration from default config file
cfg = InstaCfg(default_cfg)
dl_cfg = cfg.config.get(ConfigConstants.DOWNLOADS, {})
dl_dir = dl_cfg.get(ConfigConstants.DL_DIR, default_download_dir)
record_file_name = dl_cfg.get(ConfigConstants.RECORDS, default_records_file)


class NegateAction(argparse.Action):
    def __call__(self, parser, ns, values, option):
        setattr(ns, self.dest, option[2:4] != 'no')


class CliArgParse:

    PARSER = cfg.config.get(ConfigConstants.PARSERS)
    DL = PARSER.get(ConfigConstants.DOWNLOAD, "dl")
    INV = PARSER.get(ConfigConstants.INVENTORY, 'inv')
    QUERY = PARSER.get(ConfigConstants.QUERY, 'query')
    UI = PARSER.get(ConfigConstants.UI, 'ui')

    def __init__(self):
        # -------------------------------------------------------------------------
        # Instantiate parser
        # -------------------------------------------------------------------------
        self.parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.RawTextHelpFormatter(
            prog, width=140))

        # Define Global parser flags
        # -------------------------------------------------------------------------
        self.parser.add_argument("-c", "--cfg", default=default_cfg,
                                 help=f"Specify config file. Default: '{default_cfg}'")

        self.parser.add_argument("-d", "--debug", action="store_true", default=False,
                                 help="Enable debugging")

        # Build subparsers
        # -------------------------------------------------------------------------
        subparser = self.parser.add_subparsers(help="InstaGrab Operations", dest='parser')

        # -------------------------------------------------------------------------
        # DOWNLOADS
        # -------------------------------------------------------------------------
        downloads = subparser.add_parser(self.DL, help="   Download Media")
        # downloads.add_argument("-d", "--download", action="store_true",
        #                        help="Start listener for downloading, using copy buffer")
        downloads.add_argument('-r', '--rec_file', default=record_file_name,
                               help=f"Name of record file to track media. Default = '{record_file_name}'")
        downloads.add_argument('-l', '--location', default=dl_dir,
                               help=f"Relative root location for DL'd media. Default = '{dl_dir}'")

        # -------------------------------------------------------------------------
        # INVENTORY
        # -------------------------------------------------------------------------
        inventory = subparser.add_parser(self.INV, help="   Scan Inventory")
        # inventory.add_argument("-i", "--inventory", action="store_true",
        #                        help="Take inventory of existing files")
        inventory.add_argument('-r', '--rec_file', default=record_file_name,
                               help=f"Name of record file to track media. Default = '{record_file_name}'")

        inventory.add_argument('-l', '--location', default=dl_dir,
                               help=f"Relative root location for DL'd media. Default = '{dl_dir}'")

        # -------------------------------------------------------------------------
        # QUERY
        # -------------------------------------------------------------------------
        media_list = BuildInventory.MEDIA_TYPES.keys()
        query = subparser.add_parser(self.QUERY, help="   Query Inventory")
        query.add_argument('-f', '--filename', default=None, help="Get information on specific media file.")
        query.add_argument('--favorites', '--no-favorites', dest='favorites', default=None, action=NegateAction,
                           nargs=0, help="List/Do not list favorites")
        query.add_argument('-m', '--media_type', default=None, choices=media_list,
                           help=f"List based on selected media type")
        query.add_argument('-k', '--keyword', default=None, help="Search path name based on keyword")
        query.add_argument('-r', '--rec_file', default=record_file_name,
                           help=f"Name of record file to track media. Default = '{record_file_name}'")
        query.add_argument('-l', '--location', default=dl_dir,
                           help=f"Relative root location for DL'd media. Default = '{dl_dir}'")

        # -------------------------------------------------------------------------
        # UI
        # -------------------------------------------------------------------------
        ui = subparser.add_parser(self.UI, help="   Start the UI")
        ui.add_argument('-r', '--rec_file', default=record_file_name,
                        help=f"Name of record file to track media. Default = '{record_file_name}'")
        ui.add_argument('-l', '--location', default=dl_dir,
                        help=f"Relative root location for DL'd media. Default = '{dl_dir}'")

        # -------------------------------------------------------------------------
        # PARSE COMMAND LINE ARGUMENTS
        # -------------------------------------------------------------------------
        self._args = self.parser.parse_args()

        if self._args.parser is None:
            self._args.rec_file = record_file_name
            self._args.location = dl_dir

    def get_args(self):
        return self._args
