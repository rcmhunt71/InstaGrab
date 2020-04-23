import sys

# Window Imports
from PyQt5.QtWidgets import QApplication, QMainWindow

# Widget Imports
from PyQt5.QtWidgets import QWidget

# Control Imports

from instagrab.config.cfg import InstaCfg
from instagrab.config.config_const import ConfigConstants


class InstaGrabMainUI(QMainWindow):

    WIDTH = 400
    HEIGHT = 400

    def __init__(self, height: int = 0, width: int = 0):
        super().__init__()

        height = self.HEIGHT if height == 0 else height
        width = self.WIDTH if width == 0 else width

        self.setWindowTitle("InstaGrab")
        self.setFixedSize(width, height)

        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)


def start_ui(cfg: InstaCfg = None):

    width = 0
    height = 0
    if cfg is not None:
        width = cfg.get_element([ConfigConstants.UI, ConfigConstants.WIDTH], width)
        height = cfg.get_element([ConfigConstants.UI, ConfigConstants.HEIGHT], height)

    print(f"H: {height}   W: {width}")

    insta_grab_app = QApplication(sys.argv)
    view = InstaGrabMainUI(width=width, height=height)
    view.show()

    sys.exit(insta_grab_app.exec())
