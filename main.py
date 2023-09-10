import sys
import time
import atexit
import subprocess
from qtpy import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QProgressBar, QMessageBox, QFontDialog


class VideoSubtitleJoiner(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('BurnSub')
        self.setGeometry(100, 100, 400, 250)

        layout = QVBoxLayout()

        self.video_path_label = QLabel('Video File:')
        layout.addWidget(self.video_path_label)

        self.video_path_button = QPushButton('Select Video')
        self.video_path_button.clicked.connect(self.select_video)
        layout.addWidget(self.video_path_button)

        self.subtitle_path_label = QLabel('Subtitle File (SRT):')
        layout.addWidget(self.subtitle_path_label)

        self.subtitle_path_button = QPushButton('Select Subtitle')
        self.subtitle_path_button.clicked.connect(self.select_subtitle)
        layout.addWidget(self.subtitle_path_button)

        self.font_button = QPushButton('Choose Subtitle Font')
        self.font_button.clicked.connect(self.choose_font)
        layout.addWidget(self.font_button)

        self.subtitle_label = QLabel()
        layout.addWidget(self.subtitle_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.join_button = QPushButton('Join Video and Subtitle')
        self.join_button.clicked.connect(self.join_video_subtitle)
        layout.addWidget(self.join_button)

        self.setLayout(layout)

        atexit.register(self.cleanup)

    def select_video(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_dialog = QFileDialog()
        video_path, _ = file_dialog.getOpenFileName(self, 'Select Video File', '', 'Video Files (*.mp4 *.avi *.mkv);;All Files (*)', options=options)
        if video_path:
            self.video_path_label.setText(f'Video File: {video_path}')
            self.video_path = video_path

    def select_subtitle(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_dialog = QFileDialog()
        subtitle_path, _ = file_dialog.getOpenFileName(self, 'Select Subtitle File', '', 'SRT Files (*.srt);;All Files (*)', options=options)
        if subtitle_path:
            self.subtitle_path_label.setText(f'Subtitle File (SRT): {subtitle_path}')
            self.subtitle_path = subtitle_path

    def get_total_frames(self):
        try:
            cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of default=nokey=1:noprint_wrappers=1 "{self.video_path}"'
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            total_frames = int(result.strip())
            return total_frames
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None

    def join_video_subtitle(self):
        if hasattr(self, 'video_path') and hasattr(self, 'subtitle_path'):
            output_path, _ = QFileDialog.getSaveFileName(self, 'Save Joined Video', '', 'Video Files (*.mp4);;All Files (*)')
            if output_path:
                cmd = f'ffmpeg -y -i "{self.video_path}" -vf "subtitles={self.subtitle_path}" "{output_path}"'
                try:
                    self.ffmpeg_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
                except Exception as e:
                    QMessageBox.warning(self, 'Warning', f'Failed to join Video and Subtitle {e}')

                total_frames = self.get_total_frames()
                while self.ffmpeg_process.poll() is None:
                    output_line = self.ffmpeg_process.stdout.readline()
                    if 'frame=' in output_line:
                        parts = output_line.split()
                        frame_number = parts[1]
                        if frame_number.isdigit():
                            frame_number = int(frame_number)
                            self.progress_bar.setValue(int(frame_number/total_frames*100))
                        QtWidgets.QApplication.processEvents()

                    time.sleep(0.1)

                if self.ffmpeg_process.returncode == 0:
                    self.progress_bar.setValue(100)
                    QMessageBox.information(self, 'Success', 'Video and Subtitle joined successfully.')
                else:
                    QMessageBox.critical(self, 'Error', 'Failed to join Video and Subtitle.')
        else:
            QMessageBox.warning(self, 'Warning', 'Please select both video and subtitle files.')

    def cleanup(self):
        if hasattr(self, 'ffmpeg_process') and self.ffmpeg_process.poll() is None:
            self.ffmpeg_process.terminate()
            self.ffmpeg_process.wait()

    def choose_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.subtitle_label.setFont(font)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoSubtitleJoiner()
    window.show()
    sys.exit(app.exec_())
