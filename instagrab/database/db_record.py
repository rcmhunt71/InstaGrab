from instagrab.inventory.media_record import MediaRecord, MediaTypes

import elasticsearch7_dsl as es_dsl


class MediaRecordDoc(es_dsl.Document):
    name = es_dsl.Text()
    media_type = es_dsl.Text()
    url = es_dsl.Text()
    image_name = es_dsl.Text()
    image_data = es_dsl.Binary()
    group = es_dsl.Text()
    category = es_dsl.Text()
    favorite = es_dsl.Boolean()


class DatabaseDocument:

    MAX_RECORDS = 1000

    def __init__(self, index):
        self._index = index
        self.doc = None
        MediaRecordDoc.init(index=index)

    def set_index(self, index, reinitialize=False):
        self._index = index
        if reinitialize:
            MediaRecordDoc(self._index)

    def add_record(self, record):
        self.doc = MediaRecordDoc(
            media_type=record.media_type.value,
            name=record.name if record.name is not None else '',
            url=record.url,
            image_name=record.media_file_name,
            image_data=open(record.paths[0], "rb").read(),
            **record.metadata,
        )
        self.doc.save(index=record.db_index)
        return self.doc

    def get_inventory(self):
        return es_dsl.Search(index=self._index).extra(size=self.MAX_RECORDS).execute()

    def get_record_by_id(self, id_):
        return self.doc.get(id=id_, index=self._index)

    def get_record_by_name(self, image_name, index=None):
        index = index or self._index
        es_record = record = None
        results = es_dsl.Search(index=index).query("match", image_name=image_name).execute()

        try:
            es_record = results.hits[0]
            record = self._serialize_into_media_record(self.get_record_by_id(es_record.meta.id))

        except AttributeError as err:
            print(f"Image name not found: {image_name}")
            print(err)

        return record, es_record, results

    def _serialize_into_media_record(self, record):
        metadata = {}
        mapped_attributes = ['name', 'url', 'media_type', 'image_name', 'image_data', 'meta']
        for attrib in dir(record):
            if not attrib.startswith("_") and attrib not in mapped_attributes:
                metadata[attrib] = getattr(record, attrib)

        return MediaRecord(
            name=record.name, url=record.url, paths=[], db_index=self._index, metadata=metadata,
            media_type=MediaTypes.get_media_type_enum(record.media_type), image_data=record.image_data,
            media_file_name=record.image_name,
        )
