from datetime import datetime

from elasticsearch7 import Elasticsearch


class ESClient:
    def __init__(self, host="127.0.0.1", port=9200, credentials=None):
        self._host = host
        self._port = port
        self._creds = credentials
        self.client = Elasticsearch()

    def add_image(self, image_dict):
        pass


if __name__ == "__main__":
    from instagrab.app_utils.app_routines import inventory
    from instagrab.config.cfg import InstaCfg
    from instagrab.config.config_const import ConfigConstants
    from random import randint
    import pprint

    def choose_random_image():
        num_records = len(inv.inv)
        choice = randint(0, num_records)
        image_name = list(inv.inv.keys())[choice]
        print(f"{choice}:{num_records} --> TARGET: {image_name}")
        return image_name

    default_cfg = "../../instagrab.yml"
    default_records_file = "../../insta_media_names.txt"
    default_download_dir = '../../DLd'

    cfg = InstaCfg(cfg_file=default_cfg)
    standard_extensions = cfg.get_element(path=[ConfigConstants.EXTENSIONS], default=[])

    client = ESClient()
    inv = inventory(records_file=default_records_file, download_dir=default_download_dir,
                    file_ext_list=standard_extensions, cfg=cfg)

    target = choose_random_image()
    print(inv.inv[target])


# ---------------------------------------------------------------
    TEST = False
    if TEST:
        es = Elasticsearch()

        doc = {
            'author': 'kimchy',
            'text': 'Elasticsearch: cool. bonsai cool.',
            'timestamp': datetime.now(),
        }
        res = es.index(index="test-index", id=1, body=doc)
        print(f"RESULT: {res['result']}")

        res = es.get(index="test-index", id=1)
        print(f"SOURCE: {res['_source']}")

        es.indices.refresh(index="test-index")

        res = es.search(index="test-index", body={"query": {"match_all": {}}})
        print("Got %d Hits:" % res['hits']['total']['value'])
        for hit in res['hits']['hits']:
            print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

