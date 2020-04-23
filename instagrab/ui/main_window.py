import sys

# PyQT5 Core Imports
from PyQt5.QtCore import Qt

# PyQT5 Window Imports
from PyQt5.QtWidgets import QApplication, QMainWindow

# PyQT5 Widget Layouts
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QButtonGroup

# PyQT5 Widget Imports
from PyQt5.QtWidgets import QWidget

# PyQT5 Control Imports

from instagrab.config.cfg import InstaCfg
from instagrab.config.config_const import ConfigConstants


class InstaGrabMainUI(QMainWindow):

    WIDTH = 400
    HEIGHT = 400

    def __init__(self, cfg: InstaCfg = None, height: int = 0, width: int = 0):
        super().__init__()

        self.cfg = cfg

        height = self.HEIGHT
        width = self.WIDTH
        if self.cfg is not None:
            width, height = self._get_dimensions([ConfigConstants.UI, ConfigConstants.GENERAL])
        print(f"MAIN -> H: {height}   W: {width}")

        self.setWindowTitle("InstaGrab")
        self.setFixedSize(width, height)
        self.generalLayout = QVBoxLayout()

        self._centralWidget = QWidget(self)
        self._centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(self._centralWidget)

        self._createDisplay()
        self._createButtons()

    def _get_dimensions(self, path):

        width_path = path.copy()
        width_path.append(ConfigConstants.WIDTH)
        height_path = path.copy()
        height_path.append(ConfigConstants.HEIGHT)

        width = self.cfg.get_element(path=width_path, default=self.WIDTH)
        height = self.cfg.get_element(path=height_path, default=self.HEIGHT)
        return width, height

    def _createButtons(self):
        pass

    def _createDisplay(self):
        width = height = 200
        if self.cfg is not None:
            width, height = self._get_dimensions(path=[ConfigConstants.UI, ConfigConstants.DOWNLOAD])
        print(f"DL DISPLAY -> H: {height}   W: {width}")
        self.dl_msg_box = QLineEdit()
        self.dl_msg_box.setFixedSize(width, height)
        self.dl_msg_box.setAlignment(Qt.AlignLeft)
        self.dl_msg_box.setReadOnly(True)
        self.generalLayout.addWidget(self.dl_msg_box)


def start_ui(cfg: InstaCfg = None):
    insta_grab_app = QApplication(sys.argv)
    view = InstaGrabMainUI(cfg=cfg)
    view.show()

    sys.exit(insta_grab_app.exec())
