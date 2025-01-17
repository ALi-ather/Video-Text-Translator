import os
from deep_translator import GoogleTranslator
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QFileDialog, QTextEdit, QProgressBar, QWidget, QMessageBox
)
from PyQt6.QtCore import QThread, pyqtSignal

# Worker class for translation processing
class TranslationWorker(QThread):
    progress_update = pyqtSignal(int)
    log_update = pyqtSignal(str)

    def __init__(self, input_folder, output_folder, source_lang="en", target_lang="ar"):
        super().__init__()
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.translator = GoogleTranslator(source=self.source_lang, target=self.target_lang)

    def run(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        srt_files = [f for f in os.listdir(self.input_folder) if f.endswith(".srt")]
        total_files = len(srt_files)

        if not srt_files:
            self.log_update.emit("No .srt files found in the input folder.")
            return

        for idx, srt_file in enumerate(srt_files):
            input_srt_path = os.path.join(self.input_folder, srt_file)
            output_srt_path = os.path.join(self.output_folder, srt_file)
            
            try:
                self.log_update.emit(f"Processing file: {srt_file}")
                with open(input_srt_path, "r", encoding="utf-8") as file:
                    lines = file.readlines()

                translated_lines = []

                for line in lines:
                    if line.strip() and not line.strip().isdigit() and "-->" not in line:
                        try:
                            translated_text = self.translator.translate(line.strip())
                            translated_lines.append(translated_text + "\n")
                        except Exception as e:
                            self.log_update.emit(f"Error translating line: {line.strip()} ({e})")
                            translated_lines.append(line)
                    else:
                        translated_lines.append(line)

                with open(output_srt_path, "w", encoding="utf-8") as file:
                    file.writelines(translated_lines)

                self.log_update.emit(f"Translated and saved: {output_srt_path}")
            except Exception as e:
                self.log_update.emit(f"Error processing file {srt_file}: {e}")

            progress = int((idx + 1) / total_files * 100)
            self.progress_update.emit(progress)

# Main application class
class SRTTranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SRT Translator")
        self.setGeometry(300, 200, 600, 400)

        self.input_folder = ""
        self.output_folder = ""

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label_status = QLabel("Select input and output folders to start.")
        layout.addWidget(self.label_status)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        btn_select_input = QPushButton("Select Input Folder")
        btn_select_input.clicked.connect(self.select_input_folder)
        layout.addWidget(btn_select_input)

        btn_select_output = QPushButton("Select Output Folder")
        btn_select_output.clicked.connect(self.select_output_folder)
        layout.addWidget(btn_select_output)

        btn_start = QPushButton("Start Translation")
        btn_start.clicked.connect(self.start_translation)
        layout.addWidget(btn_start)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if folder:
            self.input_folder = folder
            self.label_status.setText(f"Input Folder: {folder}")

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder = folder
            self.label_status.setText(f"Output Folder: {folder}")

    def start_translation(self):
        if not self.input_folder or not self.output_folder:
            QMessageBox.warning(self, "Warning", "Please select both input and output folders.")
            return

        self.worker = TranslationWorker(self.input_folder, self.output_folder)
        self.worker.progress_update.connect(self.progress_bar.setValue)
        self.worker.log_update.connect(self.update_log)
        self.worker.start()

    def update_log(self, message):
        self.log_text.append(message)

if __name__ == "__main__":
    app = QApplication([])
    window = SRTTranslatorApp()
    window.show()
    app.exec()
