import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QToolBar, QLabel, QWidget, QPushButton, QLineEdit
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QFormLayout
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

default_index = 6
try:
    exercise = int(sys.argv[1])
except IndexError:
    exercise = default_index
    print(f"Need to specify exercise number (1-5). Defaulting to: {exercise}")

app = QApplication(sys.argv)

if exercise == 1:
    window = QWidget()
    window.setWindowTitle('PyQT5 App')
    name = sys.argv[2]
    window.setGeometry(100, 100, 200, 80)
    window.move(60, 15)
    helloMsg = QLabel(f'<h1>Hello {name}!</h1>', parent=window)
    helloMsg.move(10, 15)
    window.show()

elif exercise == 2:
    window = QWidget()
    window.setWindowTitle('PyQT5 App')
    layout = QHBoxLayout()
    layout.addWidget(QPushButton('Left'))
    layout.addWidget(QPushButton('Center'))
    layout.addWidget(QPushButton('Right'))
    window.setLayout(layout)
    window.show()

elif exercise == 3:
    window = QWidget()
    window.setWindowTitle('PyQT5 App')
    layout = QVBoxLayout()
    layout.addWidget(QPushButton('Top'))
    layout.addWidget(QPushButton('Middle'))
    layout.addWidget(QPushButton('Bottom'))
    window.setLayout(layout)
    window.show()

elif exercise == 4:
    window = QWidget()
    window.setWindowTitle('PyQT5 App')
    layout = QGridLayout()
    span = False
    for row in range(3):
        for column in range(3):
            if row == 2 and column > 0 and not span:
                span = True
                layout.addWidget(QPushButton(f'Button ({row},{column}) + 2 columns span'), row, column, 1, 2)
            elif not span:
                layout.addWidget(QPushButton(f'Button ({row},{column})'), row, column)
    window.setLayout(layout)
    window.show()

elif exercise == 5:
    window = QWidget()
    window.setWindowTitle('PyQT5 App')
    layout = QFormLayout()
    entries = ['Name', 'Age', 'Job', 'Hobbies']
    for entry in entries:
        layout.addRow(f'{entry}:', QLineEdit())
    window.setLayout(layout)
    window.show()

elif exercise == 6:
    class Dialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Chris' QDialog Box")
            dlgLayout = QVBoxLayout()
            formLayout = QFormLayout()
            formLayout.addRow('Name:', QLineEdit())
            formLayout.addRow('Age:', QLineEdit())
            formLayout.addRow('Job:', QLineEdit())
            formLayout.addRow('Hobbies:', QLineEdit())

            dlgLayout.addLayout(formLayout)

            btns = QDialogButtonBox()
            btns.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
            dlgLayout.addWidget(btns)
            self.setLayout(dlgLayout)

    dlg = Dialog()
    dlg.show()

elif exercise == 7:
    class Window(QMainWindow):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Chris' Main Window App")
            self.setCentralWidget(QLabel("I'm the CENTRAL widget."))
            self._createMenu()
            self._createToolBar()
            self._createStatusBar()

        def _createMenu(self):
            self.menu = self.menuBar().addMenu("&Menu")
            self.menu.addAction("&Exit", self.close)

        def _createToolBar(self):
            tools = QToolBar()
            self.addToolBar(tools)
            tools.addAction('Exit', self.close)

        def _createStatusBar(self):
            status = QStatusBar()
            status.showMessage("I'm the status bar")
            self.setStatusBar(status)

    win = Window()
    win.show()

sys.exit(app.exec())


# TUTORIAL: https://realpython.com/python-pyqt-gui-calculator/ --> Up to Dialogs
