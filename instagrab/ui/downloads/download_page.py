from PyQt5.QtWidgets import QGridLayout, QPushButton, QLabel, QPlainTextEdit
from PyQt5.QtGui import QImage, QPixmap, QMovie, QFont
from PyQt5.QtCore import Qt

from instagrab.config.config_const import ConfigConstants as CfgConsts
from instagrab.ui.ui_utilities import UiUtils

# TODO: Document (docstring and inlines) + typing + class level


class DownloadPage:

    QUEUE_IMAGE_DELIMITER = "||"
    DEFAULT_PANE_WIDTH_RATIO = 0.50
    DEFAULT_PANE_HEIGHT_RATIO = 0.75
    DEFAULT_BORDER = 10

    ENGINE_ON = "Stop Downloads"
    ENGINE_OFF = "Start Downloads"

    def __init__(self, parent, title=None):
        self.parent = parent
        self.include_title = title is not None

        self.layout = QGridLayout()
        self.engine_button = self._define_check_push_button(initial_state=self.ENGINE_OFF)
        self.title_field = self._define_title_field(title)
        self.image_view = self._define_image_view()
        self.dl_info_view = self._define_dl_info_view(text='')

        self._create_download_page()

    def _create_download_page(self):
        row_span = col_span = 4

        #                        widget,     X,    Y,    R_SPAN,    C_SPAN
        self.layout.addWidget(self.dl_info_view, int(self.include_title), 0, row_span, col_span)
        self.layout.addWidget(self.image_view, int(self.include_title), col_span, row_span, col_span)
        self.layout.addWidget(self.engine_button, int(self.include_title) + row_span, 0)

        if self.include_title:
            self.layout.addWidget(self.title_field, 0, 0)

    @staticmethod
    def _define_title_field(title):
        title = title or "Title Not Set"
        return QLabel(str(title))

    @staticmethod
    def _define_check_push_button(initial_state, width=200, height=40, checked=False):
        button = QPushButton(initial_state)
        button.setFixedSize(width, height)
        button.setCheckable(True)
        button.setChecked(checked)
        style_sheet = ("QPushButton{background-color:lightgreen;}" 
                       "QPushButton:checked{background-color:rgb(255, 184, 196);}")
        button.setStyleSheet(style_sheet)
        return button

    def _define_dl_info_view(self, text=None):
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

        dl_info = QPlainTextEdit()
        dl_info.setFixedSize(text_width, text_height)
        dl_info.setReadOnly(True)
        if text is not None:
            dl_info.insertPlainText(text)

        font = QFont()
        font.setFamily("Courier New")

        doc = dl_info.document()
        doc.setDefaultFont(font)

        return dl_info

    def _define_image_view(self):
        image = QLabel()
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
        image.setAlignment(Qt.AlignCenter)
        image.setAutoFillBackground(True)

        return image

    def update_download_info(self, text):
        # Normal text from DL process - updates the msg text label.
        if not text.startswith(self.QUEUE_IMAGE_DELIMITER):
            self.dl_info_view.insertPlainText(f"{text}\n")
            self.dl_info_view.update()

        # Detected File Msg delimiter. This will update the image QLabel.
        else:
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
