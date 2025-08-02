from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QTextEdit, QApplication

def launch_startup_script_editor(script_path=None):
    app = QApplication.instance() or QApplication([])

    window = QMainWindow()
    window.setWindowTitle("Startup Script Editor")
    central = QWidget()
    layout = QVBoxLayout(central)

    text_edit = QTextEdit()
    layout.addWidget(text_edit)

    save_button = QPushButton("Save")
    layout.addWidget(save_button)

    # Optionally load script contents
    if script_path:
        try:
            with open(script_path, "r") as f:
                text_edit.setPlainText(f.read())
        except Exception:
            pass

    def save_script():
        if script_path:
            with open(script_path, "w") as f:
                f.write(text_edit.toPlainText())

    save_button.clicked.connect(save_script)

    window.setCentralWidget(central)
    window.resize(600, 400)
    window.show()
    if not QApplication.instance():
        app.exec()
    return window