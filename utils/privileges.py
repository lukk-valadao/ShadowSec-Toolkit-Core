# utils/privileges.py
import os
import sys
import platform

def require_root():
    system = platform.system().lower()

    if system == "windows":
        # Windows será tratado depois (admin check via ctypes)
        return

    # Linux / Unix
    if os.geteuid() != 0:
        print("\n[!] Privilégios insuficientes.")
        print("    Este módulo requer execução como root.")
        print("\n👉 Execute assim:")
        print("   sudo python3 main.py\n")
        sys.exit(1)

