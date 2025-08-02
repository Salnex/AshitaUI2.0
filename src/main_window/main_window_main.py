import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
from src.Layouts.main_window_layout import create_main_layout, create_menu_bar
from src.main_window.ashita_installer.ashita_installer_main import download_and_extract_ashita
from src.config_editor.config_editor_main import launch_config_editor
from src.startup_script_editor.startup_script_editor_main import launch_startup_script_editor
from src.config import ASHITA_BOOT_CONFIG_DIR, ASHITA_SCRIPTS_DIR

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AshitaUI2.0")
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        (layout, self.dropdown, self.modify_button, self.new_button,
         self.script_dropdown, self.script_modify_button, self.script_new_button) = create_main_layout(central_widget)

        menubar, exit_action, about_action, download_button = create_menu_bar(self)
        self.setMenuBar(menubar)
        download_button.triggered.connect(self.handle_download_and_extract_ashita)
        exit_action.triggered.connect(self.close)
        about_action.triggered.connect(
            lambda: QMessageBox.information(self, "About", "An Ashita V4 UI\nVersion 2.0")
        )
        download_button.triggered.connect(self.handle_download_and_extract_ashita)

        self.modify_button.clicked.connect(self.open_modify_config)
        self.new_button.clicked.connect(self.open_new_config)
        self.script_modify_button.clicked.connect(self.open_modify_script)
        self.script_new_button.clicked.connect(self.open_new_script)
        

    def handle_download_and_extract_ashita(self):
        try:
            download_and_extract_ashita()
            QMessageBox.information(self, "Success", "Ashita downloaded and extracted!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed: {e}")
    def open_modify_config(self):
        ini_name = self.dropdown.currentText()
        ini_path = ASHITA_BOOT_CONFIG_DIR+ini_name
        self.config_editor_window = launch_config_editor(ini_path=ini_path)

    def open_new_config(self):
        self.config_editor_window = launch_config_editor(ini_path="src/Ashita-v4beta-main/config/boot/example-privateserver.ini")

    def open_modify_script(self):
        script_name = self.script_dropdown.currentText()
        script_path = os.path.join(ASHITA_SCRIPTS_DIR, script_name)
        self.startup_script_editor_window = launch_startup_script_editor(script_path=script_path)

    def open_new_script(self):
        # Create a new script file with default content
        new_script_name = "new_script.txt"
        script_path = os.path.join(ASHITA_SCRIPTS_DIR, new_script_name)
        if not os.path.exists(script_path):
            with open(script_path, "w") as f:
                f.write("# Enter your startup script here\n")
        self.startup_script_editor_window = launch_startup_script_editor(script_path=script_path)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
