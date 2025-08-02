from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from src.Layouts.config_editor_layout import create_config_editor_layout
import os
from src.Data.ini_data import ini_structure
def launch_config_editor(ini_path=None, ini_data=None):
    from PyQt6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])

    window = QMainWindow()
    central = QWidget()

    config_data = None
    if ini_path and os.path.exists(ini_path):
        import configparser
        config = configparser.ConfigParser()
        config.read(ini_path)
        config_data = {s: dict(config.items(s)) for s in config.sections()}
    elif ini_data:
        config_data = ini_data

    layout, tabs, save_button, widget_refs = create_config_editor_layout(central, config_data)
    window.setCentralWidget(central)
    window.setWindowTitle("Ashita Config Editor")
    window.show()
    if not QApplication.instance():
        app.exec()
    return window