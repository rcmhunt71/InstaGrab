import random


from instagrab.database.db_record import DatabaseDocument
from instagrab.inventory.media_record import MediaMetadata

from elasticsearch7_dsl.connections import connections

MAX_RESULTS = 1000
connections.create_connection(hosts=['localhost'])

if __name__ == "__main__":
    from instagrab.app_utils.app_routines import inventory
    from instagrab.config.cfg import InstaCfg
    from instagrab.config.config_const import ConfigConstants
    from random import randint

    default_cfg = "../../instagrab.yml"
    default_records_file = "../../insta_media_names.txt"
    default_download_dir = '../../DLd'

    def get_random_record():
        cfg = InstaCfg(cfg_file=default_cfg)
        standard_extensions = cfg.get_element(path=[ConfigConstants.EXTENSIONS], default=[])

        inv = inventory(records_file=default_records_file, download_dir=default_download_dir,
                        file_ext_list=standard_extensions, cfg=cfg)
        target = choose_random_image_name(inv=inv)
        return inv.inv[target]

    def choose_random_image_name(inv):
        num_records = len(inv.inv)
        choice = randint(0, num_records)
        image_name = list(inv.inv.keys())[choice]
        return image_name


    record = get_random_record()
    db_interface = DatabaseDocument(index=record.db_index)
    doc = db_interface.add_record(record)
    print(doc)
    print(doc.image_name)

    query = db_interface.get_inventory()

    BY_NAME = True
    BY_ID = False

    if BY_NAME:
        filename = '72571404_2153205441650534_3209203742217764885_n.jpg'
        ret_doc, es_record, results = db_interface.get_record_by_name(image_name=filename)
        if ret_doc is not None:
            # print(ret_doc.image_data)
            ext = filename.split('.')[-1]
            with open(f"chris.{ext}", "wb") as OUT:
                OUT.write(ret_doc.image_data)
            print(f"WROTE: chris.{ret_doc.media_type.value}")
            print(f"INDEX: {record.db_index}")
            # print(f"FAVORITE: {ret_doc.favorite}")
            print(f"DL: {ret_doc.metadata[MediaMetadata.GROUP]}\\"
                  f"{ret_doc.metadata[MediaMetadata.CATEGORY]}\\{ret_doc.media_file_name}")
            print(ret_doc)

    if BY_ID:
        total = query.hits.total.value
        index = random.randint(0, total - 1)
        print(f"RANDOMIZED INDEX: {index} of {total}")

        target_id = query.hits[index].meta.id
        print(f"TARGET ID: {target_id}")

        ret_doc = db_interface.get_record_by_id(target_id)
        with open(f"chris.{ret_doc.media_type}", "wb") as OUT:
            OUT.write(ret_doc.image)
        print(f"WROTE: chris.{ret_doc.media_type}")
        print(f"INDEX: {record.db_index}")
        print(f"FAVORITE: {ret_doc.favorite}")
        print(f"DL: {ret_doc.group}\\{ret_doc.category}\\{ret_doc.image_name}")
