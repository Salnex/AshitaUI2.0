import os
from src.config import ASHITA_BOOT_CONFIG_DIR, ASHITA_SCRIPTS_DIR

def get_boot_config_files():
    if not os.path.isdir(ASHITA_BOOT_CONFIG_DIR):
        return []
    return [f for f in os.listdir(ASHITA_BOOT_CONFIG_DIR) if os.path.isfile(os.path.join(ASHITA_BOOT_CONFIG_DIR, f))]

def get_script_files():
    if not os.path.isdir(ASHITA_SCRIPTS_DIR):
        return []
    return [f for f in os.listdir(ASHITA_SCRIPTS_DIR) if f.endswith('.txt')]