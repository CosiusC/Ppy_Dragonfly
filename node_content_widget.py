from PySide2.QtWidgets import *


class QDFNodeContentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()


    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.wdg_label = QLabel("Some title")
        self.layout.addWidget(self.wdg_label)
        self.layout.addWidget(QTextEdit("foo"))

        self.setObjectName("node_content_widget")
        self.wdg_label.setObjectName("node_content_widget")

        with open("./style.css", "r+") as cssFile:
            style = cssFile.read()
            self.setStyleSheet(style)
