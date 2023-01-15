from PyQt5.QtWidgets import *
import gui
import sys


if __name__ == '__main__':

    app = QApplication([])
    Window = gui.Window()
    sys.exit(app.exec())


