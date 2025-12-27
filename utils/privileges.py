import os
import sys
import platform
import ctypes

def require_root():
    """
    Verifica se o script possui privilégios administrativos (root no Linux ou Admin no Windows).
    Caso não possua, encerra a execução com uma mensagem instrutiva.
    """
    system = platform.system().lower()

    if system == "windows":
        # Verificação de privilégios de Administrador no Windows
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            is_admin = False

        if not is_admin:
            print("\n[!] Privilégios insuficientes.")
            print("    Este toolkit requer execução como Administrador no Windows.")
            print("\n👉 Abra o PowerShell/CMD como Administrador e tente novamente.\n")
            sys.exit(1)

    else:
        # Verificação de Root para Linux / Unix / Android
        # os.geteuid() verifica o ID do usuário efetivo (0 é sempre root)
        if hasattr(os, 'geteuid') and os.geteuid() != 0:
            print("\n[!] Privilégios insuficientes.")
            print("    Este módulo requer execução como root.")
            print("\n👉 Execute assim:")
            print("    sudo python3 main.py\n")
            sys.exit(1)

def is_root() -> bool:
    """Retorna True se o usuário tiver privilégios máximos, False caso contrário."""
    system = platform.system().lower()
    if system == "windows":
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    return os.geteuid() == 0 if hasattr(os, 'geteuid') else False
