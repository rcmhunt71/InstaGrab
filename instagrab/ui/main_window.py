from functools import partial
import sys

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from instagrab.config.cfg import InstaCfg
from instagrab.config.config_const import ConfigConstants as CfgConsts
from instagrab.ui.downloads.download_page import DownloadPage
from instagrab.ui.downloads.dl_controller import DLController, DLInfoListener
from instagrab.ui.ui_utilities import UiUtils


# TODO: Document (docstring and inlines) + typing + class level

class InstaGrabMainUI(QMainWindow):
    DEFAULT_WIDTH = 400
    DEFAULT_HEIGHT = 400

    def __init__(self, cfg: InstaCfg = None, height: int = 0, width: int = 0):
        super().__init__()

        self.cfg = cfg
        height = height if height > 0 else self.DEFAULT_HEIGHT
        width = width if width > 0 else self.DEFAULT_WIDTH

        if self.cfg is not None:
            width, height = UiUtils.get_dimensions(cfg, [CfgConsts.UI, CfgConsts.GENERAL])
        print(f"MAIN -> H: {height}   W: {width}")

        self.setWindowTitle("InstaGrab")
        self.setFixedSize(width, height)

        # Define Download Tab
        self.download_page = DownloadPage(parent=self, title="Download Images")

        self.dl_widget = QWidget()
        self.dl_layout = QVBoxLayout()
        self.dl_layout.addLayout(self.download_page.layout)
        self.dl_widget.setLayout(self.dl_layout)

        # Define Classification Tab
        self.classification_widget = QWidget()
        self.classification_layout = QVBoxLayout()
        self.classification_widget.setLayout(self.classification_layout)

        # Define Query Tab
        self.query_widget = QWidget()
        self.query_layout = QVBoxLayout()
        self.query_widget.setLayout(self.query_layout)

        # Define (and assemble) Tabbed Viewer
        self._centralWidget = QTabWidget(self)
        self._centralWidget.addTab(self.dl_widget, "Downloads")
        self._centralWidget.addTab(self.classification_widget, "Classification")
        self._centralWidget.addTab(self.query_widget, "Browsing")
        self.setCentralWidget(self._centralWidget)



def start_ui(dl_engine, cfg: InstaCfg = None):
    insta_grab_app = QApplication(sys.argv)
    view = InstaGrabMainUI(cfg=cfg)
    view.show()

    # Add Download View DL_INFO listener/updater.
    # add_dl_info_update_listener(view, dl_engine)
    dl_controller = DLController(dl_view=view.download_page, model=dl_engine)
    dl_info_thread = QThread()

    dl_info_update = DLInfoListener(queue=dl_controller.model.dl_resp_queue)
    dl_info_update.update_line_edit_signal.connect(view.download_page.update_download_info)
    dl_info_update.moveToThread(dl_info_thread)

    dl_info_thread.started.connect(dl_info_update.run)
    dl_info_thread.start()

    sys.exit(insta_grab_app.exec())
