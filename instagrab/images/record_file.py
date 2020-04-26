import os
from queue import Queue
import typing


class MediaRecords:
    """
    Record keeping utility to track names of items (media filenames)
    * Stores in text file: <id>|<metadata>
    """
    DELIMITER = "|"
    UNKNOWN = "Unknown"

    def __init__(self, record_file) -> typing.NoReturn:
        self.record_file = record_file

    def get_file_name_dict(self) -> typing.Dict[str, str]:
        """
        Read records from file.
        If file does not exist, returns empty dictionary.

        :return: Dictionary of {id: metadata}

        """
        if not os.path.exists(self.record_file):
            return {}

        with open(self.record_file, "r") as RECORDS:
            lines = RECORDS.readlines()
        print(f"Read records from: {self.record_file}")

        records = {}
        for line in lines:
            if line != "\n":
                if self.DELIMITER in line:
                    filename, url_str = line.split(self.DELIMITER)
                    records[filename.strip()] = url_str.strip()
                else:
                    records[line] = self.UNKNOWN.strip()

        print(f"Records processed: {len(lines)}")
        return records

    def record_file_names(self, record_dict: typing.Dict[str, str], msg_queue: Queue = None) -> typing.NoReturn:
        """
        Write all records to file (list format).

        :param record_dict: Dictionary of records {id: metadata}
        :param msg_queue: Msg queue for UI interactions (default=None)

        :return: None

        """
        with open(self.record_file, "w") as RECORDS:
            for name, location_url in record_dict.items():
                RECORDS.write(f"{name}{self.DELIMITER}{location_url}\n")
        msg = f"\nWrote {len(record_dict.keys())} records to: {self.record_file}\n"
        print(msg, flush=True)

        if msg_queue is not None:
            msg_queue.put(msg)
