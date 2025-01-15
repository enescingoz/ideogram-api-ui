# Name: Enes Cingoz
# GitHub: https://github.com/enescingoz


import sys
import os
import json
import requests
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QComboBox, QTextEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QScrollArea
)
from PyQt5.QtCore import Qt

class FuturisticUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IDEOGRAM API WITH UI")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #1e1e2e; color: #c0caf5; font-family: 'Arial'; font-size: 14px;")

        # Main Layout
        main_layout = QVBoxLayout()

        # API Key Section
        api_layout = QHBoxLayout()
        self.api_key_input = QLineEdit(self)
        self.api_key_input.setPlaceholderText("Enter your API key...")
        self.api_key_input.setStyleSheet("background-color: #2e2e4e; border: 1px solid #c0caf5; padding: 5px; font-size: 16px;")
        self.api_key_input.setText(self.load_api_key())
        api_save_btn = QPushButton("Save API Key", self)
        api_save_btn.setStyleSheet("background-color: #414868; border-radius: 5px; padding: 5px; font-size: 16px;")
        api_save_btn.clicked.connect(self.save_api_key)
        api_layout.addWidget(self.api_key_input)
        api_layout.addWidget(api_save_btn)
        main_layout.addLayout(api_layout)

        # Magic Prompt Option
        self.magic_prompt_label = QLabel("Magic Prompt Option:")
        self.magic_prompt_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.magic_prompt_combo = QComboBox(self)
        self.magic_prompt_combo.addItems(["AUTO", "ON", "OFF"])
        self.magic_prompt_combo.setStyleSheet("background-color: #2e2e4e; padding: 5px; font-size: 16px;")
        main_layout.addWidget(self.magic_prompt_label)
        main_layout.addWidget(self.magic_prompt_combo)

        # Aspect Ratio
        self.aspect_ratio_label = QLabel("Aspect Ratio:")
        self.aspect_ratio_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.aspect_ratio_combo = QComboBox(self)
        aspect_ratios = [
            "ASPECT_10_16", "ASPECT_16_10", "ASPECT_9_16", "ASPECT_16_9",
            "ASPECT_3_2", "ASPECT_2_3", "ASPECT_4_3", "ASPECT_3_4",
            "ASPECT_1_1", "ASPECT_1_3", "ASPECT_3_1"
        ]
        self.aspect_ratio_combo.addItems(aspect_ratios)
        self.aspect_ratio_combo.setStyleSheet("background-color: #2e2e4e; padding: 5px; font-size: 16px;")
        main_layout.addWidget(self.aspect_ratio_label)
        main_layout.addWidget(self.aspect_ratio_combo)

        # Model
        self.model_label = QLabel("Model:")
        self.model_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.model_combo = QComboBox(self)
        self.model_combo.addItems(["V_1", "V_1_TURBO", "V_2", "V_2_TURBO"])
        self.model_combo.setStyleSheet("background-color: #2e2e4e; padding: 5px; font-size: 16px;")
        main_layout.addWidget(self.model_label)
        main_layout.addWidget(self.model_combo)

        # Prompt Input
        self.prompt_label = QLabel("Prompt:")
        self.prompt_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.prompt_input = QTextEdit(self)
        self.prompt_input.setStyleSheet("background-color: #2e2e4e; padding: 10px; font-size: 16px;")
        main_layout.addWidget(self.prompt_label)
        main_layout.addWidget(self.prompt_input)

        # Submit Button
        submit_button = QPushButton("Send Request", self)
        submit_button.setStyleSheet("background-color: #414868; border-radius: 5px; padding: 10px; font-size: 16px;")
        submit_button.clicked.connect(self.send_request)
        main_layout.addWidget(submit_button)

        # Console Output
        self.console = QScrollArea(self)
        self.console.setWidgetResizable(True)
        self.console_widget = QTextEdit(self)
        self.console_widget.setReadOnly(True)
        self.console_widget.setStyleSheet("background-color: #2e2e4e; padding: 10px; font-size: 16px;")
        self.console.setWidget(self.console_widget)
        main_layout.addWidget(QLabel("Console:"))
        main_layout.addWidget(self.console)

        # Central Widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def load_api_key(self):
        if os.path.exists("api_key.txt"):
            with open("api_key.txt", "r") as file:
                return file.read().strip()
        return ""

    def save_api_key(self):
        api_key = self.api_key_input.text().strip()
        with open("api_key.txt", "w") as file:
            file.write(api_key)
        self.log_to_console("API key saved.")

    def send_request(self):
        api_key = self.api_key_input.text().strip()
        if not api_key:
            self.log_to_console("Error: API key is required.")
            return

        url = "https://api.ideogram.ai/generate"
        payload = {
            "image_request": {
                "prompt": self.prompt_input.toPlainText().strip(),
                "aspect_ratio": self.aspect_ratio_combo.currentText(),
                "model": self.model_combo.currentText(),
                "magic_prompt_option": self.magic_prompt_combo.currentText()
            }
        }
        headers = {"Api-Key": api_key, "Content-Type": "application/json"}

        self.log_to_console("Waiting for response...")
        time.sleep(2)
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response_data = response.json()

            if "data" in response_data and response_data["data"]:
                first_result = response_data["data"][0]
                self.log_to_console(f"URL: {first_result['url']}")
                details = (
                    f"Prompt: {first_result['prompt']}\n"
                    f"Style: {first_result['style_type']}\n"
                    f"Resolution: {first_result['resolution']}\n"
                    f"Seed: {first_result['seed']}\n"
                    f"Image Safe: {first_result['is_image_safe']}\n"
                )
                self.log_to_console(details)
            else:
                self.log_to_console("No data in response.")
        except Exception as e:
            self.log_to_console(f"Error: {str(e)}")

    def log_to_console(self, message):
        self.console_widget.append(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FuturisticUI()
    window.show()
    sys.exit(app.exec_())
