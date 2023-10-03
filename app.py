from PyQt5.QtCore import QLocale
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QLabel, QLineEdit,
                             QPushButton, QWidget)

from converter import Converter


class App(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()
    
    def initUI(self):
        mainLayout = QGridLayout(self)

        self.input_folder = QLineEdit('input')
        mainLayout.addWidget(self.input_folder, 0, 1)

        input_label = QLabel('Input folder')
        input_label.setBuddy(self.input_folder)
        mainLayout.addWidget(input_label, 0, 0)

        self.output_folder = QLineEdit('output')
        mainLayout.addWidget(self.output_folder, 1, 1)

        output_label = QLabel('Output folder')
        output_label.setBuddy(self.output_folder)
        mainLayout.addWidget(output_label, 1, 0)

        mainLayout.addWidget(self.initLoadUI(), 2, 0)
        mainLayout.addWidget(self.initConvertUI(), 2, 1)

        self.setWindowTitle('Image Processing')
        self.show()

    def initLoadUI(self) -> QGroupBox:
        group = QGroupBox('Load')
        mainLayout = QGridLayout()

        self.count_text = QLineEdit('1000')
        self.count_text.setValidator(QIntValidator(0, 9999999))
        mainLayout.addWidget(self.count_text, 0, 1)

        count_label = QLabel('Count')
        count_label.setBuddy(self.count_text)
        mainLayout.addWidget(count_label, 0, 0)

        load_button = QPushButton("Load random images")
        load_button.clicked.connect(self.load_random_images)
        mainLayout.addWidget(load_button, 1, 0, 1, 2)

        group.setLayout(mainLayout)
        return group

    def initConvertUI(self) -> QGroupBox:
        group = QGroupBox('Convert')
        mainLayout = QGridLayout()

        self.sharpness_text = QLineEdit('1')
        self.sharpness_text.setValidator(QDoubleValidator(0, 99999, 10))
        mainLayout.addWidget(self.sharpness_text, 0, 1)

        sharpness_label = QLabel('Sharpness factor')
        sharpness_label.setBuddy(self.sharpness_text)
        mainLayout.addWidget(sharpness_label, 0, 0)

        self.scale_text = QLineEdit('0.5')
        validator = QDoubleValidator(0, 99999, 10)
        validator.setLocale(QLocale('en_US'))
        self.scale_text.setValidator(validator)
        mainLayout.addWidget(self.scale_text, 1, 1)

        scale_label = QLabel('Scale factor')
        scale_label.setBuddy(self.scale_text)
        mainLayout.addWidget(scale_label, 1, 0)

        convert_button = QPushButton("Convert images")
        convert_button.clicked.connect(self.convert_images)
        mainLayout.addWidget(convert_button, 2, 0, 1, 2)

        group.setLayout(mainLayout)
        return group

    def load_random_images(self):
        Converter.load_images(int(self.count_text.text()), self.input_folder.text())

    def convert_images(self):
        Converter.convert_images(
            float(self.sharpness_text.text()),
            float(self.scale_text.text()),
            self.input_folder.text(),
            self.output_folder.text())
