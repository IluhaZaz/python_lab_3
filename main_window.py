import sys
import os

from PyQt5 import QtWidgets

from task_5 import Iterator
import task_1
import task_2
import task_3


class ScrollLabel(QtWidgets.QScrollArea):
    def __init__(self, *args, **kwargs) -> None:
        QtWidgets.QScrollArea.__init__(self, *args, **kwargs)
        self.setWidgetResizable(True)
        text = QtWidgets.QWidget(self)
        self.setWidget(text)
        lay = QtWidgets.QVBoxLayout(text)
        self.label = QtWidgets.QLabel(text)
        self.label.setWordWrap(True)
        lay.addWidget(self.label)

    def setText(self, text):
        self.label.setText(text)


class Window(QtWidgets.QWidget):
    def __init__(self) -> None:
        super(QtWidgets.QWidget, self).__init__()
        self.initUI()
        self.setStyleSheet(
            "background:rgb(255,239,213); color: rgb(48, 48, 48); font-weight:bold; border-radius: 5px;")


    def initUI(self) -> None:
        self.choose_dir_button = QtWidgets.QPushButton(self)
        self.choose_dir_button.setText("Select dataset folder")
        self.choose_dir_button.adjustSize()
        self.choose_dir_button.clicked.connect(self.choose_dir)
        self.choose_dir_button.setStyleSheet("background:rgb(255,218,185); border: 5px solid rgb(255,218,185)")

        self.dir_label = QtWidgets.QLabel(self)
        self.dir_label.setText("")
        self.dir_label.adjustSize()

        self.create_ann_btn = QtWidgets.QPushButton(self)
        self.create_ann_btn.setText("Create annotation for your dataset")
        self.create_ann_btn.adjustSize()
        self.create_ann_btn.clicked.connect(self.create_annotation)
        self.create_ann_btn.setStyleSheet("background:rgb(255,218,185);  border: 5px solid rgb(255,218,185)")

        self.ann_success_label = QtWidgets.QLabel(self)

        self.good_button = QtWidgets.QPushButton(self)
        self.good_button.setText("Show next good review")
        self.good_button.adjustSize()
        self.good_button.clicked.connect(self.get_next_good)
        self.good_button.setStyleSheet("background:rgb(255,218,185);  border: 5px solid rgb(255,218,185)")

        self.review_label = ScrollLabel(self)
        self.review_label.setStyleSheet("background:rgb(255,228,181);  border: 5px solid rgb(255,218,185)")

        self.bad_button = QtWidgets.QPushButton(self)
        self.bad_button.setText("Show next bad review")
        self.bad_button.adjustSize()
        self.bad_button.clicked.connect(self.get_next_bad)
        self.bad_button.setStyleSheet("background:rgb(255,218,185);  border: 5px solid rgb(255,218,185)")

        self.copy_dataset_btn = QtWidgets.QPushButton(self)
        self.copy_dataset_btn.setText("Create dataset with different struct")
        self.copy_dataset_btn.adjustSize()
        self.copy_dataset_btn.clicked.connect(self.copy_dataset)
        self.copy_dataset_btn.setStyleSheet("background:rgb(255,218,185);  border: 5px solid rgb(255,218,185)")

        self.random_dataset_btn = QtWidgets.QPushButton(self)
        self.random_dataset_btn.setText("Create dataset with random instances")
        self.random_dataset_btn.adjustSize()
        self.random_dataset_btn.clicked.connect(self.create_rand_dataset)
        self.random_dataset_btn.setStyleSheet("background:rgb(255,218,185);  border: 5px solid rgb(255,218,185)")

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(7)
        grid.addWidget(self.choose_dir_button, 1, 0)
        grid.addWidget(self.dir_label, 1, 1)
        grid.addWidget(self.create_ann_btn, 2, 0)
        grid.addWidget(self.ann_success_label, 2, 1)
        grid.addWidget(self.good_button, 3, 0)
        grid.addWidget(self.bad_button, 5, 0)
        grid.addWidget(self.review_label, 3, 1, 3, 1)
        grid.addWidget(self.copy_dataset_btn, 6, 0)
        grid.addWidget(self.random_dataset_btn, 7, 0)
        self.setLayout(grid)

        self.setWindowTitle("3rd lab")
        self.setGeometry(0, 0, 1900, 950)


    def choose_dir(self) -> None:
        self.dataset_path = os.path.abspath(
            QtWidgets.QFileDialog.getExistingDirectory(self, "Select dataset folder")
        )
        self.dir_label.setText(f"Chose directory: {self.dataset_path}")
        self.dir_label.adjustSize()
        self.good_iterator = Iterator(self.dataset_path, "good")
        self.bad_iterator = Iterator(self.dataset_path, "bad")


    def create_annotation(self) -> None:
        try:
            if task_1.create_annotaion("ann1.csv", self.dataset_path) == True:
                self.ann_success_label.setText("Success")
            else:
                self.ann_success_label.setText("Error")
        except AttributeError:
            self.error_window("You should choose directory first!", "Error")


    def get_next_good(self) -> None:
        try:
            with open(next(self.good_iterator), "r", encoding="utf-8") as file:
                self.review_label.setText(" ".join(file.readlines()))
        except AttributeError:
            self.error_window("You should choose directory first!", "Error")
        except IndexError:
            self.review_label.setText("Комментарии закончились")
            self.good_iterator =  Iterator(self.dataset_path, "good")


    def get_next_bad(self) -> None:
        try:
            with open(next(self.bad_iterator), "r", encoding="utf-8") as file:
                self.review_label.setText(" ".join(file.readlines()))
        except AttributeError:
            self.error_window("You should choose directory first!", "Error")
        except IndexError:
            self.review_label.setText("Комментарии закончились")
            self.bad_iterator =  Iterator(self.dataset_path, "bad")


    def copy_dataset(self) -> None:
        try:
            self.copy_dir = os.path.abspath(
                QtWidgets.QFileDialog.getExistingDirectory(
                    self, "Select dataset copy folder"
                )
            )
            task_2.copy_dataset(self.copy_dir, self.dataset_path)
            task_2.create_annotaion(self.copy_dir, self.dataset_path, "ann2.csv")
        except AttributeError:
            self.error_window("You should choose directory first!", "Error")


    def error_window(self, text, title)->None:
        dialog = QtWidgets.QDialog()

        label = QtWidgets.QLabel(dialog)
        label.setText(text)
        label.adjustSize()

        btn = QtWidgets.QPushButton(dialog)
        btn.setText("Ok")
        btn.adjustSize()
        btn.move(50, 50)
        btn.clicked.connect(lambda: dialog.hide())
        btn.setStyleSheet("background:rgb(255,218,185);  border: 5px solid rgb(255,218,185)")

        lay = QtWidgets.QVBoxLayout()
        lay.addWidget(label)
        lay.addWidget(btn)
        dialog.setLayout(lay)

        dialog.setFixedSize(400, 200)
        dialog.setWindowTitle(title)
        dialog.setStyleSheet("background:rgb(255,239,213); color: rgb(48, 48, 48); font-weight:bold; border-radius: 5px;")
        dialog.exec_()


    def create_rand_dataset(self) -> None:
        try:
            self.copy_rand_dir = os.path.abspath(
                QtWidgets.QFileDialog.getExistingDirectory(
                    self, "Select dataset random copy folder"
                )
            )
            task_3.create_annotaion(self.copy_rand_dir, self.dataset_path, "ann3.csv")
        except AttributeError:
            self.error_window("You should choose directory first!", "Error")


def application() -> None:
    app = QtWidgets.QApplication(sys.argv)

    window = Window()

    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
