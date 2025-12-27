import platform
import sys

def get_os() -> str:
    """
    Detecta e normaliza o nome do Sistema Operacional atual.
    Retorna: 'linux', 'windows', 'android' ou 'unknown'.
    """
    try:
        current_os = platform.system().lower()

        if current_os == "linux":
            # Verifica se é Android (Android roda sobre kernel Linux)
            if hasattr(sys, 'getandroidapilevel') or "ANDROID_ROOT" in dict(sys.path[0]):
                return "android"
            return "linux"

        if current_os == "windows":
            return "windows"

        return current_os # Retorna o nome padrão (darwin, etc) se não for os acima

    except Exception:
        return "unknown"

def is_android() -> bool:
    return get_os() == "android"

def is_linux() -> bool:
    return get_os() == "linux"

def is_windows() -> bool:
    return get_os() == "windows"
