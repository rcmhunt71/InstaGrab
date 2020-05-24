import ast
import random
import sys

from instagrab.database.db_record import DatabaseDocument
from instagrab.inventory.media_record import MediaMetadata

from elasticsearch7.exceptions import NotFoundError
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

    filename = ''
    criteria = {}
    if len(sys.argv) > 1:
        BY_NAME = BY_ID = BY_CRITERIA = False

        if sys.argv[1].endswith('jpg'):
            BY_NAME = True
            filename = sys.argv[1]

        if sys.argv[1].endswith('find'):
            BY_CRITERIA = True
            criteria = sys.argv[-1]
            print(f'CRITERIA: "{criteria}"')
            criteria = ast.literal_eval(criteria)

        else:
            BY_ID = True

        db_index = 'people' if len(sys.argv) == 2 else sys.argv[-1]

        print(f"Identifying by:\n\tBY_NAME: {BY_NAME}\n\tBY_ID: {BY_ID}\n\tBY_CRITERIA: {BY_CRITERIA}")
        print(f"DB INDEX: {db_index}")

        if BY_NAME:
            try:
                ret_doc, es_record, results = db_interface.get_record_by_name(
                    image_name=filename, index=db_index)

            except NotFoundError:
                print(f"{db_index}:{filename} not found")

            else:
                if ret_doc is not None:
                    ext = filename.split('.')[-1]
                    with open(f"chris.{ext}", "wb") as OUT:
                        OUT.write(ret_doc.image_data)
                    print(f"WROTE: chris.{ret_doc.media_type.value}")
                    print(f"INDEX: {record.db_index}")
                    print(f"FAVORITE: {ret_doc.favorite}")
                    print(f"DL: {ret_doc.metadata[MediaMetadata.GROUP]}\\"
                          f"{ret_doc.metadata[MediaMetadata.CATEGORY]}\\{ret_doc.media_file_name}")
                    print(ret_doc)

        elif BY_ID:
            total = query.hits.total.value
            total = total if total > 0 else 1
            index = random.randint(0, total - 1)
            print(f"RANDOMIZED INDEX: {index} of {total}")

            target_id = query.hits[index].meta.id
            print(f"TARGET ID: {target_id}")

            try:
                ret_doc = db_interface.get_record_by_id(target_id, index=db_index)
            except NotFoundError:
                print(f"{db_index}:{target_id} not found")
            else:
                with open(f"chris.{ret_doc.media_type}", "wb") as OUT:
                    OUT.write(ret_doc.image)
                print(f"WROTE: chris.{ret_doc.media_type}")
                print(f"INDEX: {record.db_index}")
                print(f"FAVORITE: {ret_doc.favorite}")
                print(f"DL: {ret_doc.db_index}\\{ret_doc.category}\\{ret_doc.image_name}")

        elif BY_CRITERIA:
            results = db_interface.search_inventory(keyword_dict=criteria)
            print(f"NUMBER OF HITS: {len(results)}")
            for hit in results:
                print(hit)

