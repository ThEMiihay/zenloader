from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QLabel, QComboBox,
    QFileDialog, QFrame, QPushButton
)
from PySide6.QtCore import QSettings
import os

from ui.sidebar import Sidebar
from ui.dashboard import Dashboard
from core.downloader import DownloadThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ZenLoader")
        self.resize(1150, 680)

        # ================= STATE =================
        self.is_paused = False
        self.current_thread = None

        # ================= SETTINGS =================
        self.settings = QSettings("ZenLoader", "ZenLoaderApp")

        exe_dir = os.path.dirname(os.path.abspath(__file__))
        default_path = os.path.dirname(exe_dir)

        self.current_language = self.settings.value("language", "EN")
        self.current_theme = self.settings.value("theme", "Dark")

        if not self.settings.value("download_path"):
            self.settings.setValue("download_path", default_path)

        # ================= CENTRAL LAYOUT =================
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(main_layout)

        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setStyleSheet("color: #1e293b;")
        main_layout.addWidget(separator)

        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        self.dashboard = Dashboard()
        self.settings_page = self.create_settings_page()
        self.about_page = self.create_about_page()

        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.settings_page)
        self.stack.addWidget(self.about_page)

        # NAVIGATION
        self.sidebar.dashboard_btn.clicked.connect(lambda: self.switch_tab(0))
        self.sidebar.settings_btn.clicked.connect(lambda: self.switch_tab(1))
        self.sidebar.about_btn.clicked.connect(lambda: self.switch_tab(2))

        # DOWNLOAD
        self.dashboard.download_btn.clicked.connect(self.start_download)
        self.dashboard.cancel_btn.clicked.connect(self.cancel_download)
        self.dashboard.pause_btn.clicked.connect(self.toggle_pause)

        self.apply_language(self.current_language)
        self.apply_theme(self.current_theme)

    # =====================================================
    # TAB SWITCH
    # =====================================================
    def switch_tab(self, index):
        self.stack.setCurrentIndex(index)
        self.sidebar.dashboard_btn.setChecked(index == 0)
        self.sidebar.settings_btn.setChecked(index == 1)
        self.sidebar.about_btn.setChecked(index == 2)

    # =====================================================
    # DOWNLOAD
    # =====================================================
    def start_download(self):
        url = self.dashboard.url_input.text().strip()
        format_type = self.format_selector.currentText()
        download_path = self.settings.value("download_path")

        if not url or not download_path:
            self.dashboard.status_label.setText("Status: Missing URL or Folder")
            return

        if self.current_thread and self.current_thread.isRunning():
            return

        self.current_thread = DownloadThread(url, download_path, format_type)

        self.current_thread.progress.connect(self.dashboard.progress_bar.setValue)
        self.current_thread.status.connect(
            lambda text: self.dashboard.status_label.setText(f"Status: {text}")
        )
        self.current_thread.log.connect(self.dashboard.add_log)

        self.current_thread.start()

        self.is_paused = False
        self.dashboard.pause_btn.setText(self.translations["pause"])

    def cancel_download(self):
        if self.current_thread and self.current_thread.isRunning():
            self.current_thread.pause()
            self.dashboard.status_label.setText("Status: Stopped")
            self.dashboard.pause_btn.setText(self.translations["pause"])
            self.is_paused = False

    def toggle_pause(self):
        if not self.current_thread:
            return

        if not self.is_paused:
            self.current_thread.pause()
            self.is_paused = True
            self.dashboard.pause_btn.setText(self.translations["resume"])
            self.dashboard.add_log("Download paused")
        else:
            self.start_download()
            self.dashboard.add_log("Download resumed")

    # =====================================================
    # SETTINGS PAGE
    # =====================================================
    def create_settings_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)
        page.setLayout(layout)

        # Theme
        self.theme_label = QLabel()
        layout.addWidget(self.theme_label)

        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["Dark", "Classic"])
        self.theme_selector.setCurrentText(self.current_theme)
        layout.addWidget(self.theme_selector)

        # Language
        self.language_label = QLabel()
        layout.addWidget(self.language_label)

        self.language_selector = QComboBox()
        self.language_selector.addItems(["EN", "RO", "DE"])
        self.language_selector.setCurrentText(self.current_language)
        layout.addWidget(self.language_selector)

        # Format
        self.format_label = QLabel()
        layout.addWidget(self.format_label)

        self.format_selector = QComboBox()
        self.format_selector.addItems(["MP3 (Audio Only)", "MP4 (Video)"])
        self.format_selector.setCurrentText("MP3 (Audio Only)")
        layout.addWidget(self.format_selector)

        # Folder title
        self.folder_title = QLabel()
        layout.addWidget(self.folder_title)

        # 🔥 Folder selector readăugat
        folder_layout = QHBoxLayout()

        self.folder_btn = QPushButton()
        self.folder_btn.clicked.connect(self.choose_folder)

        self.folder_label = QLabel(self.settings.value("download_path"))

        folder_layout.addWidget(self.folder_btn)
        folder_layout.addWidget(self.folder_label)

        layout.addLayout(folder_layout)
        layout.addStretch()

        self.theme_selector.currentTextChanged.connect(self.change_theme)
        self.language_selector.currentTextChanged.connect(self.change_language)

        return page

    # =====================================================
    # CHOOSE FOLDER
    # =====================================================
    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.settings.setValue("download_path", folder)
            self.folder_label.setText(folder)

    # =====================================================
    # ABOUT PAGE
    # =====================================================
    def create_about_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(15)
        page.setLayout(layout)

        self.about_title = QLabel("ZenLoader")
        self.about_version = QLabel("Version: 0.3(build 22426)")
        self.about_desc = QLabel("Built with PySide6 + yt-dlp")
        self.about_author = QLabel("Author: Mihai")

        layout.addWidget(self.about_title)
        layout.addWidget(self.about_version)
        layout.addWidget(self.about_desc)
        layout.addWidget(self.about_author)
        layout.addStretch()

        return page

    # =====================================================
    # THEME
    # =====================================================
    def change_theme(self, theme):
        self.settings.setValue("theme", theme)
        self.apply_theme(theme)

    def apply_theme(self, theme):
        if theme == "Dark":
            self.setStyleSheet(self.dark_theme())
        else:
            self.setStyleSheet("")

    # =====================================================
    # LANGUAGE
    # =====================================================
    def change_language(self, lang):
        self.settings.setValue("language", lang)
        self.apply_language(lang)

    def apply_language(self, lang):
        translations = {
            "EN": {
                "dashboard": "Dashboard",
                "settings": "Settings",
                "about": "About",
                "download": "Download",
                "pause": "Pause",
                "resume": "Resume",
                "cancel": "Cancel",
                "youtube": "YouTube Link:",
                "console": "Console:",
                "theme": "Theme",
                "language": "Language",
                "format": "Default Format",
                "folder": "Default Download Folder",
                "choose_folder": "Choose Folder"
            },
            "RO": {
                "dashboard": "Panou",
                "settings": "Setări",
                "about": "Despre",
                "download": "Descarcă",
                "pause": "Pauză",
                "resume": "Continuă",
                "cancel": "Anulează",
                "youtube": "Link YouTube:",
                "console": "Consolă:",
                "theme": "Temă",
                "language": "Limbă",
                "format": "Format Implicit",
                "folder": "Folder Descărcare",
                "choose_folder": "Alege Folder"
            },
            "DE": {
                "dashboard": "Übersicht",
                "settings": "Einstellungen",
                "about": "Über",
                "download": "Herunterladen",
                "pause": "Pause",
                "resume": "Fortsetzen",
                "cancel": "Abbrechen",
                "youtube": "YouTube Link:",
                "console": "Konsole:",
                "theme": "Thema",
                "language": "Sprache",
                "format": "Standardformat",
                "folder": "Download-Ordner",
                "choose_folder": "Ordner wählen"
            },
        }

        self.translations = translations.get(lang, translations["EN"])
        t = self.translations

        self.sidebar.dashboard_btn.setText(t["dashboard"])
        self.sidebar.settings_btn.setText(t["settings"])
        self.sidebar.about_btn.setText(t["about"])

        self.dashboard.url_label.setText(t["youtube"])
        self.dashboard.console_label.setText(t["console"])
        self.dashboard.download_btn.setText(t["download"])
        self.dashboard.pause_btn.setText(t["pause"])
        self.dashboard.cancel_btn.setText(t["cancel"])

        self.theme_label.setText(t["theme"])
        self.language_label.setText(t["language"])
        self.format_label.setText(t["format"])
        self.folder_title.setText(t["folder"])
        self.folder_btn.setText(t["choose_folder"])

    # =====================================================
    # DARK THEME
    # =====================================================
    def dark_theme(self):
        return """
        QMainWindow {
            background-color: #0b1120;
        }

        QWidget {
            color: #e2e8f0;
            font-size: 14px;
        }

        #sidebar {
            background-color: #0f172a;
        }

        QPushButton {
            border-radius: 20px;
            padding: 10px;
            border: none;
        }

        QPushButton:hover {
            background-color: #1e293b;
        }

        QPushButton:checked {
            background-color: #1e293b;
            font-weight: 600;
        }

        QPushButton#downloadBtn {
            background-color: #22c55e;
            color: white;
        }

        QPushButton#downloadBtn:hover {
            background-color: #16a34a;
        }

        QPushButton#pauseBtn {
            background-color: #eab308;
            color: black;
        }

        QPushButton#pauseBtn:hover {
            background-color: #ca8a04;
        }

        QPushButton#cancelBtn {
            background-color: #ef4444;
            color: white;
        }

        QPushButton#cancelBtn:hover {
            background-color: #dc2626;
        }

        QLineEdit, QTextEdit {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 8px;
            selection-background-color: #22c55e;
        }

        QProgressBar {
            background-color: #1e293b;
            border-radius: 10px;
            text-align: center;
        }

        QProgressBar::chunk {
            background-color: #22c55e;
            border-radius: 10px;
        }
        """