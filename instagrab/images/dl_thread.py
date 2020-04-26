import queue
import sys
import threading
import time
import typing

import pyperclip

from instagrab.images.image_dl import GetMedia
from instagrab.images.record_file import MediaRecords


sys.stdout.flush()

# TODO: Document (docstring and inlines) + typing + class level


class ThreadedDL:
    QUEUE_SIZE = 5

    def __init__(self, record_file: str = None, flush_records: int = 5, download_dir: str = None,
                 reporting_widget=None) -> typing.NoReturn:
        self.record_file = record_file
        self.flush_records = flush_records
        self.download_dir = download_dir
        self.reporting_widget = reporting_widget
        self.dl_thread = None
        self.thread_control_queue = queue.Queue(maxsize=self.QUEUE_SIZE)
        self.dl_resp_queue = queue.Queue()
        self.running = False
        self.all_records = {}
        self.media_records = None
        self.has_dl = False

    def _msg(self, msg):
        print(msg)
        self.dl_resp_queue.put(msg)

    def start_listening(self):
        if not self.running:
            self.running = True
            self.dl_thread = threading.Thread(
                target=self._dl_media, daemon=True,
                args=(self.record_file, self.flush_records, self.download_dir, self.thread_control_queue))
            self.dl_thread.start()
            self.thread_control_queue.put_nowait(self.running)

    def stop_listening(self):
        self.running = False
        self.thread_control_queue.put_nowait(self.running)

    def _dl_media(self, record_file, flush_records, download_dir, dl_queue):

        running = True
        old_url = None
        dl_total = 0

        # Clear copy buffer of any old contents
        pyperclip.copy('')

        self.media_records = MediaRecords(record_file=record_file)
        self.all_records = self.media_records.get_file_name_dict()

        # -----------------------------------
        # Until signaled to stop
        # -----------------------------------
        while running:

            if not dl_queue.empty():
                running = dl_queue.get()
                if not running:
                    if self.has_dl:
                        self.media_records.record_file_names(
                            record_dict=self.all_records, msg_queue=self.dl_resp_queue)
                    else:
                        self._msg("No downloads detected.")
                    self._msg("DL Engine is off...")

            # -----------------------------------
            # Get the URL from the copy buffer (non-blocking)
            # -----------------------------------
            try:
                url = pyperclip.waitForPaste(0.25)
            except pyperclip.PyperclipTimeoutException:
                continue

            # -----------------------------------
            # Make sure the text from the buffer is a new/unique URL
            # -----------------------------------
            if url == old_url or url is None or not url.startswith('http'):
                time.sleep(0.25)
                continue

            # -----------------------------------
            # Get the media info (url, name, etc.)
            # -----------------------------------
            media = GetMedia(url_str=url, relative_dir=download_dir)

            # -----------------------------------
            # If the media file has not be DL'd, get the media file and
            # record that the media files have been DL'd so name list is written to file.
            # -----------------------------------
            if media.name not in self.all_records:
                dl_total += 1
                media.set_index(dl_total)
                self.all_records[media.name] = media.url

                # Download the target media from the provided URL
                try:
                    media.download_media(msg_queue=self.dl_resp_queue)
                    old_url = media.url

                except Exception as exc:
                    self.media_records.record_file_names(self.all_records)
                    self._msg(f"ERROR: {exc}")
                    dl_total -= 1

                # Write all of the metadata to file after flush_records DLs
                else:
                    self.has_dl = True
                    if dl_total % flush_records == 0:
                        self.media_records.record_file_names(self.all_records, msg_queue=self.dl_resp_queue)

            # if the file has the media file name but not the URL, save the URL
            elif self.all_records[media.name] == MediaRecords.UNKNOWN:
                self.all_records[media.name] = media.url
                self._msg(f"URL updated for {media.name}")

            # -----------------------------------
            # Duplicate media file (it was found in the list), so don't DL the media file.
            # -----------------------------------
            else:
                self._msg(f"NOTE: Media file '{media.name}' has already been downloaded.")
                old_url = media.url
