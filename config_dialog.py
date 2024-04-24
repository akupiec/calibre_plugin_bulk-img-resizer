from qt.core import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QIntValidator, Qt, QHBoxLayout


class ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.max_resolution = 1080
        self.quality = 100
        self.covert_to_webp = None

        self.setWindowTitle("Bulk Image Resizer")
        layout = QVBoxLayout()

        info_label = QLabel("<b>Attention!</b>")
        info_label2 = QLabel("There are height compression options! Try default one's before proceeding.")
        info_label.setTextFormat(Qt.RichText)
        info_label.setAlignment(Qt.AlignCenter)
        info_label2.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
        layout.addWidget(info_label2)
        layout.addSpacing(10)
        layout.addStretch(1)

        label1 = QLabel('Please indicate the maximum resolution for images (applied to the shorter side):')
        self.input1 = QLineEdit()
        self.input1.setValidator(QIntValidator(500, 4000))
        self.input1.setText(str(self.max_resolution))
        layout.addWidget(label1)
        layout.addWidget(self.input1)

        label2 = QLabel('Please indicate the quality for webp codec conversion (it is ok to keep it at 100%):')
        self.input2 = QLineEdit()
        self.input2.setValidator(QIntValidator(50, 100))
        self.input2.setText(str(self.quality))
        layout.addWidget(label2)
        layout.addWidget(self.input2)

        self.checkbox = QCheckBox('Use WebP compression (unsupported by Kindle!)')
        layout.addWidget(self.checkbox)

        button_layout = QHBoxLayout()
        submit_button = QPushButton('OK')
        submit_button.clicked.connect(self.submit)
        button_layout.addWidget(submit_button)

        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def submit(self):
        self.max_resolution = int(self.input1.text())
        self.quality = int(self.input2.text())
        self.covert_to_webp = self.checkbox.isChecked()
        self.accept()
