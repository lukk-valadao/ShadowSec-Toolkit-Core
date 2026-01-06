# utils/privileges.py
import os
import platform

def require_root() -> bool:
    system = platform.system().lower()

    if system == "windows":
        return True  # será tratado depois

    return os.geteuid() == 0
