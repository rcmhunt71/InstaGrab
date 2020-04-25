from functools import partial

# TODO: Document (docstring and inlines) + typing + Class Level


class DLController:
    def __init__(self, dl_view, model):
        self._view = dl_view
        self.model = model
        self._connect_signals()

    def _connect_signals(self):
        self._view.start_button.clicked.connect(self.model.start_listening)
        self._view.stop_button.clicked.connect(self.model.stop_listening)
