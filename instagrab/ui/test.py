import sys

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QLineEdit
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QFormLayout

app = QApplication(sys.argv)

try:
    exercise = int(sys.argv[1])
except Exception:
    exercise = 5
    print(f"Need to specify exercise number (1-5). Defaulting to: {exercise}")

window = QWidget()
window.setWindowTitle('PyQT5 App')

if exercise == 1:
    name = sys.argv[2]
    window.setGeometry(100, 100, 200, 80)
    window.move(60, 15)
    helloMsg = QLabel(f'<h1>Hello {name}!</h1>', parent=window)
    helloMsg.move(10, 15)

elif exercise == 2:
    layout = QHBoxLayout()
    layout.addWidget(QPushButton('Left'))
    layout.addWidget(QPushButton('Center'))
    layout.addWidget(QPushButton('Right'))
    window.setLayout(layout)

elif exercise == 3:
    layout = QVBoxLayout()
    layout.addWidget(QPushButton('Top'))
    layout.addWidget(QPushButton('Middle'))
    layout.addWidget(QPushButton('Bottom'))
    window.setLayout(layout)

elif exercise == 4:
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

elif exercise == 5:
    layout = QFormLayout()
    entries = ['Name', 'Age', 'Job', 'Hobbies']
    for entry in entries:
        layout.addRow(f'{entry}:', QLineEdit())
    window.setLayout(layout)

window.show()
sys.exit(app.exec_())

# TUTORIAL: https://realpython.com/python-pyqt-gui-calculator/ --> Up to Dialogs
