from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

import sys
import os

from task_5 import Iterator

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("3rd lab")
        self.setGeometry(0, 0, 1920, 1080)

        self.good_review = QtWidgets.QLabel(self)
        self.good_review.move(50, 50)
        self.good_review.setText("akoakoks")
        self.good_review.adjustSize()
        self.good_review.setWordWrap(True)

        self.good_button = QtWidgets.QPushButton(self)
        self.good_button.setText("Show next good review")
        self.good_button.adjustSize()
        self.good_button.clicked.connect(self.get_next_good)

        self.bad_review = QtWidgets.QLabel(self)
        self.bad_review.move(800, 50)
        self.bad_review.setText("DAADSFAWSFSA")
        self.bad_review.adjustSize()
        self.bad_review.setWordWrap(True)
        print()

        self.bad_button = QtWidgets.QPushButton(self)
        self.bad_button.move(800, 0)
        self.bad_button.setText("Show next bad review")
        self.bad_button.adjustSize()
        self.bad_button.clicked.connect(self.get_next_bad)

        self.good_iterator = Iterator(os.path.join("c:\\", "Users", "Acer", "Documents", "py_lab_1", "dataset"), "good")
        self.bad_iterator = Iterator(os.path.join("c:\\", "Users", "Acer", "Documents", "py_lab_1", "dataset"), "bad")

    def get_next_good(self):
        with open(next(self.good_iterator), "r", encoding="utf-8") as file:
            self.good_review.setText(" ".join(file.readlines()))
            self.good_review.adjustSize()

    def get_next_bad(self):
        with open(next(self.bad_iterator), "r", encoding="utf-8") as file:
            self.bad_review.setText(" ".join(file.readlines()))
            self.bad_review.adjustSize()


def application():
    app = QApplication(sys.argv)

    window = Window()
    
    window.show()

    sys.exit(app.exec_())
    


if __name__ == "__main__":
    application()