import sys
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon, QFontDatabase, QFont

from ui.main_window import MainWindow


# 🔥 Funcție universală pentru PyInstaller
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def load_font(app):
    font_path = resource_path("assets/SFPRODISPLAYREGULAR.OTF")

    font_id = QFontDatabase.addApplicationFont(font_path)

    if font_id != -1:
        family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(family)
        app.setFont(font)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 🔥 Icon compatibil exe
    icon_path = resource_path("assets/icon.png")

    load_font(app)

    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())