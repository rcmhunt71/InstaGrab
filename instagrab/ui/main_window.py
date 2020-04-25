import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from instagrab.config.cfg import InstaCfg
from instagrab.config.config_const import ConfigConstants as CfgConsts
from instagrab.ui.downloads.download_page import DownloadPage
from instagrab.ui.downloads.dl_controller import DLController
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
        self.generalLayout = QVBoxLayout()

        self._centralWidget = QWidget(self)
        self._centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(self._centralWidget)

        self.download_page = DownloadPage(parent=self, title="Download Images")
        self.generalLayout.addLayout(self.download_page.layout)


def start_ui(dl_engine, cfg: InstaCfg = None):
    insta_grab_app = QApplication(sys.argv)
    view = InstaGrabMainUI(cfg=cfg)
    view.show()

    DLController(dl_view=view.download_page, model=dl_engine)

    sys.exit(insta_grab_app.exec())
