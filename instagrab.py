import signal
import time
import typing

from instagrab.app_utils.app_routines import inventory, query, ui
from instagrab.cli.args import CliArgParse
from instagrab.config.cfg import InstaCfg
from instagrab.config.config_const import ConfigConstants
from instagrab.images.dl_thread import ThreadedDL

# TODO: Document app level


# -----------------------------------
# Catch the Ctrl-C, and write DL'd media names to file.
# -----------------------------------
def handler(signal_received: signal.SIGINT, frame: typing.Any):
    print("Control-C captured, exiting.")

    # If there was a file DL'd, write all metadata to file before exiting
    if dl_engine.has_dl:
        dl_engine.stop_listening()
        dl_engine.media_records.record_file_names(dl_engine.all_records)
    exit(0)


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
    standard_extensions = cfg.get_element(path=[ConfigConstants.EXTENSIONS], default=[])
    flush = cfg.get_element(path=[ConfigConstants.DOWNLOADS, ConfigConstants.WRITE_EVERY], default=None)

    # -----------------------------------
    # DOWNLOADS
    # -----------------------------------
    if args.parser == CliArgParse.DL:

        dl_engine = ThreadedDL(record_file=args.rec_file, flush_records=flush, download_dir=args.location)
        signal.signal(signal.SIGINT, handler)

        dl_engine.start_listening()
        while dl_engine.running:
            time.sleep(1)

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
        dl_engine = ThreadedDL(record_file=args.rec_file, flush_records=flush, download_dir=args.location)
        ui(records_file=args.rec_file, download_dir=args.location, cfg=cfg, dl_engine=dl_engine, debug=args.debug)

    else:
        dl_engine = ThreadedDL(record_file=args.rec_file, flush_records=flush, download_dir=args.location)
        ui(records_file=args.rec_file, download_dir=args.location, cfg=cfg, dl_engine=dl_engine, debug=args.debug)
        inventory(records_file=args.rec_file, download_dir=args.location, file_ext_list=standard_extensions, cfg=cfg)
