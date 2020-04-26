from functools import partial

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject

# TODO: Document (docstring and inlines) + typing + Class Level


class DLController:
    def __init__(self, dl_view, model):
        self._view = dl_view
        self.model = model
        self._connect_signals()

    def _connect_signals(self):
        self._view.engine_button.clicked.connect(self._dl_engine_control)

    def _dl_engine_control(self):
        # Download has been turned on, and change label to next state
        if self._view.engine_button.isChecked():
            self._view.engine_button.setText(self._view.ENGINE_ON)
            self.model.start_listening()

        # Download has been turned off, change label to next state
        else:
            self._view.engine_button.setText(self._view.ENGINE_OFF)
            self.model.stop_listening()


class DLInfoListener(QObject):
    update_line_edit_signal = pyqtSignal(str)

    def __init__(self, queue, *args, **kwargs):
        QObject.__init__(self, *args, **kwargs)
        self.queue = queue

    def run(self):
        while True:
            msg = self.queue.get()
            self.update_line_edit_signal.emit(msg)
