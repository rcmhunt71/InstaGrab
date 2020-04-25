from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QGridLayout, QPushButton
from PyQt5.QtWidgets import QLabel

from instagrab.config.config_const import ConfigConstants as CfgConsts
from instagrab.ui.ui_utilities import UiUtils


class DownloadPage:

    DEFAULT_PANE_WIDTH_RATIO = 0.50
    DEFAULT_PANE_HEIGHT_RATIO = 0.75
    DEFAULT_BORDER = 10

    def __init__(self, parent, title=None):
        self.parent = parent

        self.layout = QGridLayout()
        self.include_title = title is not None
        self.start_button = self._define_push_button("Start")
        self.stop_button = self._define_push_button("Stop")
        self.title = self._define_title(title)
        self.image = self._define_image()
        self.dl_info = self._define_dl_info()

        self._create_download_page()

    def _create_download_page(self):
        row_span = col_span = 4

        #                        widget,     X,    Y,    R_SPAN,    C_SPAN
        self.layout.addWidget(self.dl_info, int(self.include_title), 0, row_span, col_span)
        self.layout.addWidget(self.image, int(self.include_title), col_span, row_span, col_span)
        self.layout.addWidget(self.start_button, int(self.include_title) + row_span, 0)
        self.layout.addWidget(self.stop_button,  int(self.include_title) + row_span, 1)

        if self.include_title:
            self.layout.addWidget(self.title, 0, 0)

    @staticmethod
    def _define_title(title):
        title = title or "Title Not Set"
        return QLabel(str(title))

    @staticmethod
    def _define_push_button(title, width=200, height=40):
        button = QPushButton(title)
        button.setFixedSize(width, height)
        return button

    def _define_dl_info(self):
        border = self.DEFAULT_BORDER
        text_width = self.parent.DEFAULT_WIDTH * self.DEFAULT_PANE_WIDTH_RATIO
        text_height = self.parent.DEFAULT_HEIGHT * self.DEFAULT_PANE_HEIGHT_RATIO

        if self.parent.cfg is not None:
            border = self.parent.cfg.get_element(
                path=[CfgConsts.UI, CfgConsts.BORDER, CfgConsts.BORDER], default=border)

            total_width, total_height = UiUtils.get_dimensions(
                cfg=self.parent.cfg, path=[CfgConsts.UI, CfgConsts.GENERAL])

            text_width_ratio, text_height_ratio = UiUtils.get_dimensions(
                cfg=self.parent.cfg,
                path=[CfgConsts.UI, CfgConsts.DOWNLOAD, CfgConsts.TEXT, CfgConsts.RATIO])

            text_width = (total_width * text_width_ratio) - border
            text_height = (total_height * text_height_ratio) - border

        dl_info = QLineEdit()
        dl_info.setFixedSize(text_width, text_height)
        dl_info.setAlignment(Qt.AlignLeft)
        dl_info.setReadOnly(True)

        return dl_info

    def _define_image(self):
        # image = QLabel()
        image = QLineEdit()

        image_width = self.parent.DEFAULT_WIDTH * 0.5
        image_height = self.parent.DEFAULT_HEIGHT * 0.875

        border = self.parent.cfg.get_element(
            path=[CfgConsts.UI, CfgConsts.BORDER, CfgConsts.BORDER], default=10)

        if self.parent.cfg is not None:
            total_width, total_height = UiUtils.get_dimensions(
                cfg=self.parent.cfg, path=[CfgConsts.UI, CfgConsts.GENERAL])

            image_width_ratio, image_height_ratio = UiUtils.get_dimensions(
                cfg=self.parent.cfg,
                path=[CfgConsts.UI, CfgConsts.DOWNLOAD, CfgConsts.IMAGE, CfgConsts.RATIO])

            image_width = (total_width * image_width_ratio) - border
            image_height = (total_height * image_height_ratio) - border

        image.setFixedSize(image_width, image_height)
        image.setAutoFillBackground(True)

        return image
