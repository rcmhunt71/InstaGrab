from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit
from PyQt5.QtGui import QPixmap, QMovie, QImage

from instagrab.config.config_const import ConfigConstants as CfgConsts
from instagrab.ui.ui_utilities import UiUtils

class QueryPage:

    QUEUE_IMAGE_DELIMITER = "||"
    DEFAULT_PANE_WIDTH_RATIO = 0.50
    DEFAULT_PANE_HEIGHT_RATIO = 0.75
    DEFAULT_BORDER = 10

    def __init__(self, parent, title=None):
        self.parent = parent
        self.include_title = title is not None
        self.layout = QGridLayout()

        self.image_view = self._define_image_view()
        self.explorer_view = self._define_explorer_panel()

        self._create_page()
        self.update_image_viewer(self.parent.cfg.get_element([CfgConsts.TEST, CfgConsts.IMAGE], ''))

    def _create_page(self):
        self.layout.addWidget(self.explorer_view, int(self.include_title), 0, 8, 5)
        self.layout.addWidget(self.image_view, int(self.include_title), 5, 8, 10)

    def _define_image_view(self):
        image_view = QLabel()
        image_width = self.parent.DEFAULT_WIDTH * 0.5
        image_height = self.parent.DEFAULT_HEIGHT * 0.875

        border = self.parent.cfg.get_element(
            path=[CfgConsts.UI, CfgConsts.BORDER, CfgConsts.BORDER], default=10)

        if self.parent.cfg is not None:
            total_width, total_height = UiUtils.get_dimensions(
                cfg=self.parent.cfg, path=[CfgConsts.UI, CfgConsts.GENERAL])

            image_width_ratio, image_height_ratio = UiUtils.get_dimensions(
                cfg=self.parent.cfg,
                path=[CfgConsts.UI, CfgConsts.QUERY, CfgConsts.IMAGE, CfgConsts.RATIO])

            image_width = (total_width * image_width_ratio) - border
            image_height = (total_height * image_height_ratio) - border

        image_view.setFixedSize(image_width, image_height)
        image_view.setAlignment(Qt.AlignCenter)
        image_view.setAutoFillBackground(True)

        return image_view

    def _define_explorer_panel(self):
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
                path=[CfgConsts.UI, CfgConsts.QUERY, CfgConsts.VIEW, CfgConsts.RATIO])

            text_width = (total_width * text_width_ratio) - border
            text_height = (total_height * text_height_ratio) - border

        # TODO: Change this class to something appropriate
        explorer = QLineEdit()
        explorer.setFixedSize(text_width, text_height)

        return explorer

    def update_image_viewer(self, text):
        # Normal text from DL process - updates the msg text label.
        # Detected File Msg delimiter. This will update the image QLabel.

        filename = text.split(self.QUEUE_IMAGE_DELIMITER)[-1]
        if filename.endswith('jpg'):
            pix_map = QPixmap.fromImage(QImage(filename)).scaled(
                self.image_view.size(),
                aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
            self.image_view.setPixmap(pix_map)
        elif filename.endswith('mp4'):
            image = QMovie(filename)
            image.start()
        self.image_view.update()
