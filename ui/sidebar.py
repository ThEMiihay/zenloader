from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
import os


class Sidebar(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedWidth(240)
        self.setObjectName("sidebar")

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 40, 20, 20)
        self.setLayout(layout)

        base_path = os.path.dirname(os.path.dirname(__file__))
        icon_path = os.path.join(base_path, "assets", "icons")

        self.dashboard_btn = QPushButton("Dashboard")
        self.settings_btn = QPushButton("Settings")
        self.about_btn = QPushButton("About")

        self.dashboard_btn.setIcon(QIcon(os.path.join(icon_path, "dashboard.png")))
        self.settings_btn.setIcon(QIcon(os.path.join(icon_path, "settings.png")))
        self.about_btn.setIcon(QIcon(os.path.join(icon_path, "about.png")))

        for btn in [self.dashboard_btn, self.settings_btn, self.about_btn]:
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setMinimumHeight(45)
            btn.setIconSize(QSize(20, 20))
            btn.setStyleSheet("text-align: left; padding-left: 18px;")

        self.dashboard_btn.setChecked(True)

        layout.addWidget(self.dashboard_btn)
        layout.addWidget(self.settings_btn)
        layout.addWidget(self.about_btn)

        layout.addStretch()  # 🔥 împinge versiunea jos

        # 🔥 VERSION LABEL
        self.version_label = QLabel("V 0.4")
        self.version_label.setAlignment(Qt.AlignCenter)
        self.version_label.setStyleSheet("""
            color: #64748b;
            font-size: 12px;
        """)

        layout.addWidget(self.version_label)