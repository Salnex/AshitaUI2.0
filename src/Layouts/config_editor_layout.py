from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QPushButton, QFormLayout,
    QLineEdit, QCheckBox, QSpinBox, QComboBox, QLabel, QScrollArea
)
from src.Data.ini_data import ini_structure, ui_metadata, friendly_names

def create_config_editor_layout(parent, config_data=None):
    layout = QVBoxLayout(parent)
    tabs = QTabWidget()
    layout.addWidget(tabs)
    save_button = QPushButton("Save")
    layout.addWidget(save_button)

    # Organize fields by tab
    tab_fields = {}
    for section, keys in ui_metadata.items():
        for key, meta in keys.items():
            if not meta.get("show", True):
                continue
            tab_name = meta.get("tab", section)
            tab_fields.setdefault(tab_name, []).append((section, key, meta))

    # Create a QWidget for each tab, wrapped in QScrollArea
    tab_widgets = {}
    for tab_name, fields in tab_fields.items():
        tab_content = QWidget()
        form = QFormLayout(tab_content)
        form.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(tab_content)

        tab_widgets[tab_name] = (tab_content, form)
        tabs.addTab(scroll, tab_name)

    # Add widgets for each field
    widget_refs = {}
    for tab_name, fields in tab_fields.items():
        tab_content, form = tab_widgets[tab_name]
        for section, key, meta in fields:
            label = friendly_names.get(section, {}).get(key, key)
            value = ""
            if config_data and section in config_data and key in config_data[section]:
                value = config_data[section][key]
            else:
                value = ini_structure.get(section, {}).get(key, "")

            widget_type = meta.get("widget", "lineedit")
            if widget_type == "lineedit":
                w = QLineEdit()
                w.setText(str(value))
            elif widget_type == "checkbox":
                w = QCheckBox()
                w.setChecked(str(value).strip() in ("1", "true", "True"))
            elif widget_type == "spinbox":
                w = QSpinBox()
                w.setMinimum(-99999)
                w.setMaximum(99999)
                try:
                    w.setValue(int(value))
                except Exception:
                    w.setValue(0)
            elif widget_type == "combobox":
                w = QComboBox()
                valid_values = meta.get("valid_values", {})
                if isinstance(valid_values, dict):
                    for display, val in valid_values.items():
                        w.addItem(display, val)
                    idx = list(valid_values.values()).index(str(value)) if str(value) in valid_values.values() else 0
                    w.setCurrentIndex(idx)
                else:
                    w.addItem(str(value))
            else:
                w = QLabel(f"Unsupported widget: {widget_type}")
            form.addRow(label, w)
            widget_refs[(section, key)] = w

    return layout, tabs, save_button, widget_refs