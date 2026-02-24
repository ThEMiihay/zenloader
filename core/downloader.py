import yt_dlp
from yt_dlp.utils import DownloadCancelled
import os
import sys
from PySide6.QtCore import QThread, Signal


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class DownloadThread(QThread):
    progress = Signal(int)
    status = Signal(str)
    log = Signal(str)
    finished_signal = Signal()

    def __init__(self, url, download_path, format_type):
        super().__init__()
        self.url = url
        self.download_path = download_path
        self.format_type = format_type
        self._cancel_requested = False

    def run(self):

        def hook(d):
            if self._cancel_requested:
                raise DownloadCancelled()

            if d["status"] == "downloading":
                percent = d.get("_percent_str", "0%").replace("%", "").strip()
                try:
                    self.progress.emit(int(float(percent)))
                except:
                    pass

            elif d["status"] == "finished":
                filename = os.path.basename(d.get("filename", ""))
                if filename:
                    self.log.emit(f"Finished: {filename}")

        output_template = os.path.join(
            self.download_path,
            "%(playlist_title,UnknownPlaylist)s/%(title)s.%(ext)s"
        )

        ffmpeg_dir = resource_path("assets/ffmpeg")
        ffmpeg_exe = os.path.join(ffmpeg_dir, "ffmpeg.exe")
        ffprobe_exe = os.path.join(ffmpeg_dir, "ffprobe.exe")

        ffmpeg_path = (
            ffmpeg_dir
            if os.path.exists(ffmpeg_exe) and os.path.exists(ffprobe_exe)
            else None
        )

        ydl_opts = {
            "format": "best"
            if self.format_type != "MP3 (Audio Only)"
            else "bestaudio/best",
            "progress_hooks": [hook],
            "outtmpl": output_template,
            "continuedl": True,
            "quiet": True,
            "noplaylist": False,
            "ignoreerrors": True,
            "extractor_args": {
                "youtube": {
                    "player_client": ["android"]
                }
            },
            "no_warnings": True,
        }

        if ffmpeg_path:
            ydl_opts["ffmpeg_location"] = ffmpeg_path

        if self.format_type == "MP3 (Audio Only)":
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]

        try:
            self.status.emit("Downloading...")
            self.log.emit("Download started")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])

            if not self._cancel_requested:
                self.status.emit("Completed")
                self.progress.emit(100)
                self.log.emit("All downloads completed")

        except DownloadCancelled:
            self.status.emit("Cancelled")
            self.log.emit("Download cancelled by user")

        except Exception as e:
            self.status.emit("Error")
            self.log.emit(f"Error: {str(e)}")

        finally:
            self.finished_signal.emit()

    def cancel(self):
        self._cancel_requested = True