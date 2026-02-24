from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QTextEdit, QHBoxLayout,
    QProgressBar, QLabel
)
from PySide6.QtCore import Qt
from datetime import datetime


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)
        self.setLayout(layout)

        self.url_label = QLabel("YouTube Link:")
        self.url_input = QLineEdit()
        self.url_input.setMinimumHeight(40)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        self.download_btn = QPushButton("Download")
        self.download_btn.setObjectName("downloadBtn")

        self.pause_btn = QPushButton("Pause")
        self.pause_btn.setObjectName("pauseBtn")

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("cancelBtn")

        for btn in [self.download_btn, self.pause_btn, self.cancel_btn]:
            btn.setMinimumHeight(40)
            btn.setCursor(Qt.PointingHandCursor)

        button_layout.addWidget(self.download_btn)
        button_layout.addWidget(self.pause_btn)
        button_layout.addWidget(self.cancel_btn)

        self.status_label = QLabel("Status: Idle")

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        self.console_label = QLabel("Console:")
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMinimumHeight(200)

        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addLayout(button_layout)
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        layout.addSpacing(20)
        layout.addWidget(self.console_label)
        layout.addWidget(self.console)

    def add_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.append(f"[{timestamp}] {message}")