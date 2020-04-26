from functools import partial

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject

# TODO: Document (docstring and inlines) + typing + Class Level


class DLController:
    def __init__(self, dl_view, model):
        self._view = dl_view
        self.model = model
        # self.listener = DLListener(queue=model.dl_resp_queue)
        self._connect_signals()

    def _connect_signals(self):
        self._view.start_button.clicked.connect(self.model.start_listening)
        self._view.stop_button.clicked.connect(self.model.stop_listening)
        # self.listener.update_line_edit.connect(self._view.update_dl_info)


class DLInfoListener(QObject):
    update_line_edit_signal = pyqtSignal(str)

    def __init__(self, queue, *args, **kwargs):
        QObject.__init__(self, *args, **kwargs)
        self.queue = queue

    def run(self):
        while True:
            msg = self.queue.get()
            self.update_line_edit_signal.emit(msg)
