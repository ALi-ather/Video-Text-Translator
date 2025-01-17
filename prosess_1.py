import os
import subprocess
from whisper import load_model
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget, QTextEdit, QMessageBox,
    QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

# Worker Thread for Background Processing
class TranscriptionWorker(QThread):
    progress_update = pyqtSignal(int)
    log_update = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, video_folder, output_folder, model_name="base"):
        super().__init__()
        self.video_folder = video_folder
        self.output_folder = output_folder
        self.model_name = model_name

    def run(self):
        # Load Whisper model
        self.log_update.emit("Loading Whisper model...")
        model = load_model(self.model_name)

        video_files = [f for f in os.listdir(self.video_folder) if f.endswith(".ts")]
        total_files = len(video_files)

        if not video_files:
            self.log_update.emit("No video files found in the selected folder.")
            return

        for idx, filename in enumerate(video_files):
            video_path = os.path.join(self.video_folder, filename)
            audio_path = os.path.join(self.output_folder, f"{os.path.splitext(filename)[0]}.wav")
            srt_path = os.path.join(self.output_folder, f"{os.path.splitext(filename)[0]}.srt")

            try:
                self.log_update.emit(f"Processing video: {filename}")

                # Convert video to audio
                self.convert_video_to_audio(video_path, audio_path)
                
                # Transcribe audio
                self.log_update.emit("Transcribing audio...")
                segments = self.extract_text_with_timestamps(audio_path, model)

                # Save transcription to SRT file
                self.save_transcription_to_srt(segments, srt_path)
                self.log_update.emit(f"Saved transcription: {srt_path}")
            except Exception as e:
                self.log_update.emit(f"Error processing {filename}: {e}")

            # Update progress
            self.progress_update.emit(int((idx + 1) / total_files * 100))

        self.log_update.emit("All videos processed successfully!")
        self.finished.emit()

    def convert_video_to_audio(self, video_path, audio_path):
        command = [
            "ffmpeg",
            "-i", video_path,
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            audio_path
        ]
        subprocess.run(command, check=True)

    def extract_text_with_timestamps(self, audio_path, model):
        result = model.transcribe(audio_path, word_timestamps=False)
        return result["segments"]

    def save_transcription_to_srt(self, segments, srt_path):
        with open(srt_path, "w", encoding="utf-8") as f:
            for i, segment in enumerate(segments):
                start = segment["start"]
                end = segment["end"]
                text = segment["text"]

                start_time = f"{int(start // 3600):02}:{int((start % 3600) // 60):02}:{int(start % 60):02},{int((start % 1) * 1000):03}"
                end_time = f"{int(end // 3600):02}:{int((end % 3600) // 60):02}:{int(end % 60):02},{int((end % 1) * 1000):03}"

                f.write(f"{i + 1}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text.strip()}\n\n")

# Main Application Window
class VideoTranscriptionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Transcription App")
        self.setGeometry(200, 200, 600, 400)

        self.video_folder = ""
        self.output_folder = ""

        # Main Layout
        layout = QVBoxLayout()

        self.label_status = QLabel("Select video and output folders to start.")
        self.label_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_status)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.text_log = QTextEdit()
        self.text_log.setReadOnly(True)
        layout.addWidget(self.text_log)

        btn_select_video_folder = QPushButton("Select Video Folder")
        btn_select_video_folder.clicked.connect(self.select_video_folder)
        layout.addWidget(btn_select_video_folder)

        btn_select_output_folder = QPushButton("Select Output Folder")
        btn_select_output_folder.clicked.connect(self.select_output_folder)
        layout.addWidget(btn_select_output_folder)

        btn_start = QPushButton("Start Transcription")
        btn_start.clicked.connect(self.start_transcription)
        layout.addWidget(btn_start)

        # Central Widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def select_video_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Video Folder")
        if folder:
            self.video_folder = folder
            self.label_status.setText(f"Selected Video Folder: {folder}")

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder = folder
            self.label_status.setText(f"Selected Output Folder: {folder}")

    def start_transcription(self):
        if not self.video_folder or not self.output_folder:
            QMessageBox.warning(self, "Warning", "Please select both video and output folders.")
            return

        self.worker = TranscriptionWorker(self.video_folder, self.output_folder)
        self.worker.progress_update.connect(self.progress_bar.setValue)
        self.worker.log_update.connect(self.update_log)
        self.worker.finished.connect(self.transcription_finished)
        self.worker.start()

    def update_log(self, message):
        self.text_log.append(message)

    def transcription_finished(self):
        QMessageBox.information(self, "Completed", "All videos have been processed.")

if __name__ == "__main__":
    app = QApplication([])
    window = VideoTranscriptionApp()
    window.show()
    app.exec()
