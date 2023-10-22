from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget

import sys
import os

from task_5 import Iterator
from task_1 import create_annotaion

class Window(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.choose_dir_button = QtWidgets.QPushButton(self)
        self.choose_dir_button.setText("Select dataset folder")
        self.choose_dir_button.setFixedWidth(300)
        self.choose_dir_button.clicked.connect(self.choose_dir)

        self.dir_label = QtWidgets.QLabel(self)
        self.dir_label.setText("")

        self.create_ann_btn = QtWidgets.QPushButton(self)
        self.create_ann_btn.setText("Create annotation for your dataset")
        self.create_ann_btn.setFixedWidth(300)
        self.create_ann_btn.clicked.connect(self.create_annotation_for_btn)

        self.ann_success_label = QtWidgets.QLabel(self)

        self.good_button = QtWidgets.QPushButton(self)
        self.good_button.setText("Show next good review")
        self.good_button.adjustSize()
        self.good_button.clicked.connect(self.get_next_good)

        self.bad_button = QtWidgets.QPushButton(self)
        self.bad_button.move(940, 0)
        self.bad_button.setText("Show next bad review")
        self.bad_button.adjustSize()
        self.bad_button.clicked.connect(self.get_next_bad)


        grid = QGridLayout()
        grid.setSpacing(20)
        grid.addWidget(self.choose_dir_button, 0, 0)
        grid.addWidget(self.dir_label, 0, 1)
        grid.addWidget(self.create_ann_btn, 1, 0)    
        grid.addWidget(self.ann_success_label, 1, 1)
        grid.addWidget(self.good_button, 2, 0)
        grid.addWidget(self.bad_button, 3, 0)
        self.setLayout(grid)
        
        self.setWindowTitle("3rd lab")
        self.setGeometry(0, 0, 1920, 1080)

    def choose_dir(self):
        self.dataset_path = os.path.abspath(QtWidgets.QFileDialog.getExistingDirectory(self, 'Select dataset folder'))
        self.dir_label.setText(f"Chose directory: {self.dataset_path}")
        self.dir_label.adjustSize()
        self.good_iterator = Iterator(self.dataset_path, "good")
        self.bad_iterator = Iterator(self.dataset_path, "bad")
        
    def create_annotation_for_btn(self):
        if create_annotaion("ann1.csv", self.dataset_path) == True:
            self.ann_success_label.setText("Success")
        else:
            self.ann_success_label.setText("Error")
      
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