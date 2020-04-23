from instagrab.app_utils.app_routines import download_media, inventory, query, ui
from instagrab.cli.args import CliArgParse
from instagrab.config.cfg import InstaCfg
from instagrab.config.config_const import ConfigConstants


if __name__ == "__main__":

    # -----------------------------------
    # Get CLI args
    # -----------------------------------
    cli_parser = CliArgParse()
    args = cli_parser.get_args()

    if args.debug:
        from pprint import pformat
        print(f"DEBUG: CLI NAMESPACE: {pformat(args)}")

    cfg = InstaCfg(cfg_file=args.cfg)
    standard_extensions = cfg.get_element([ConfigConstants.EXTENSIONS], [])
    flush = cfg.get_element([ConfigConstants.DOWNLOADS, ConfigConstants.WRITE_EVERY], default=None)

    # -----------------------------------
    # DOWNLOADS
    # -----------------------------------
    if args.parser == CliArgParse.DL:
        download_media(record_file=args.rec_file, flush_records=flush, download_dir=args.location)

    # -----------------------------------
    # INVENTORY
    # -----------------------------------
    elif args.parser == CliArgParse.INV:
        inventory(records_file=args.rec_file, download_dir=args.location, file_ext_list=standard_extensions, cfg=cfg)

    # -----------------------------------
    # QUERIES
    # -----------------------------------
    elif args.parser == CliArgParse.QUERY:
        query(filename=args.filename, records_file=args.rec_file, download_dir=args.location,
              keyword=args.keyword, media_type=args.media_type, favorites=args.favorites,
              file_ext_list=standard_extensions, cfg=cfg, debug=args.debug)

    # -----------------------------------
    # UI
    # -----------------------------------
    elif args.parser == CliArgParse.UI:
        ui(records_file=args.rec_file, download_dir=args.location, cfg=cfg, debug=args.debug)

    # Code should never get here, because a sub-parser command directive is required and is validated by CliArgParse.
    else:
        known_args = ", " .join([f'"--{arg}"' for arg in dir(args) if not arg.startswith("_")])
        print(f"\n** ERROR **:\n\tNo recognized arguments found: {known_args}\n")
        CliArgParse().parser.print_help()
