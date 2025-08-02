from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QComboBox, QPushButton, QMenuBar, QMenu, QHBoxLayout, QToolButton, QSizePolicy
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
from src.main_window.main_window_helpers import get_boot_config_files, get_script_files

def create_icon_button(icon_name: str, tooltip: str, callback=None) -> QToolButton:
    button = QToolButton()
    icon = QIcon.fromTheme(icon_name)
    if icon.isNull():
        # Try loading from local resources/icons folder
        icon_path = f"resources/icons/{icon_name}.png"
        icon = QIcon(icon_path)
    button.setIcon(icon)
    button.setToolTip(tooltip)
    button.setCursor(Qt.CursorShape.PointingHandCursor)
    button.setStyleSheet("""
        QToolButton {
            border: none;
            padding: 0px;
            background: transparent;
        }
        QToolButton:hover {
            background: #444444;
        }
    """)
    if callback:
        button.clicked.connect(callback)
    return button

def create_main_layout(parent):
    layout = QVBoxLayout(parent)

    # Boot config controls
    dropdown_hori_layout = QHBoxLayout()
    dropdown = QComboBox()
    dropdown.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    dropdown.addItems(get_boot_config_files())
    modify_button = create_icon_button("gtk-edit", "Modify Boot Config")
    new_button = create_icon_button("gtk-add", "New Boot Config")
    dropdown_hori_layout.addWidget(dropdown)
    dropdown_hori_layout.addWidget(modify_button, alignment=Qt.AlignmentFlag.AlignRight)
    dropdown_hori_layout.addWidget(new_button, alignment=Qt.AlignmentFlag.AlignRight)
    dropdown_hori_layout.setContentsMargins(0, 0, 0, 0)
    dropdown_hori_layout.setSpacing(0)
    layout.addLayout(dropdown_hori_layout)

    # Startup script controls
    script_dropdown_layout = QHBoxLayout()
    script_dropdown = QComboBox()
    script_dropdown.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    script_dropdown.addItems(get_script_files())
    script_modify_button = create_icon_button("gtk-edit", "Modify Startup Script")
    script_new_button = create_icon_button("gtk-add", "New Startup Script")
    script_dropdown_layout.addWidget(script_dropdown)
    script_dropdown_layout.addWidget(script_modify_button, alignment=Qt.AlignmentFlag.AlignRight)
    script_dropdown_layout.addWidget(script_new_button, alignment=Qt.AlignmentFlag.AlignRight)
    script_dropdown_layout.setContentsMargins(0, 0, 0, 0)
    script_dropdown_layout.setSpacing(0)
    layout.addLayout(script_dropdown_layout)
    return layout, dropdown, modify_button, new_button, script_dropdown, script_modify_button, script_new_button

def create_menu_bar(main_window):
    menubar = QMenuBar(main_window)
    file_menu = QMenu("File", menubar)
    help_menu = QMenu("Help", menubar)
    
    menubar.addMenu(file_menu)
    menubar.addMenu(help_menu)

    exit_action = QAction("Exit", main_window)
    about_action = QAction("About", main_window)
    download_button = QAction("Install Ashita",main_window)
    file_menu.addAction(download_button)
    file_menu.addAction(exit_action)

    help_menu.addAction(about_action)

    return menubar, exit_action, about_action, download_button