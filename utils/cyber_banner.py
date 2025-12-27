import os
import time
import sys
import ctypes

# PALETA DARK CYBERPUNK (Normalizada para garantir compatibilidade)
DARK = {
    "purple":   "\033[38;2;140;0;255m",
    "violet":   "\033[38;2;170;50;220m",
    "blood":    "\033[38;2;200;0;50m",
    "magenta":  "\033[38;2;180;0;180m",
    "midnight": "\033[38;2;0;50;150m",
    "cyan":     "\033[38;2;0;180;200m",
    "orchid":   "\033[38;2;150;50;200m",
    "reset":    "\033[0m"
}

ANIM_SEQUENCE = [
    DARK["purple"], DARK["blood"], DARK["violet"],
    DARK["midnight"], DARK["magenta"], DARK["orchid"],
    DARK["cyan"], DARK["purple"]
]

UNIVERSAL_BANNER = """
    ╔══════════════════════════════════════════════════════════════╗
    ║ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ║
    ║ ▓▓     █ █ █   NEON DISTRICT MALWARE SCANNER   █ █ █      ▓▓ ║
    ║ ▓▓                                                        ▓▓ ║
    ║ ▓▓   ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗  ▓▓ ║
    ║ ▓▓   ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║  ▓▓ ║
    ║ ▓▓   ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║  ▓▓ ║
    ║ ▓▓   ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║  ▓▓ ║
    ║ ▓▓   ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝  ▓▓ ║
    ║ ▓▓   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝   ▓▓ ║
    ║ ▓▓                                                        ▓▓ ║
    ║ ▓▓            SHADOWSEC TOOLKIT CORE v1.0                 ▓▓ ║
    ║ ▓▓      システム侵入検知モードが有効になりました          ▓▓ ║
    ║ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ║
    ╚══════════════════════════════════════════════════════════════╝"""

def _init_terminal():
    """Habilita suporte a ANSI no Windows 10+"""
    if os.name == 'nt':
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

def cyber_boot(banner_text=UNIVERSAL_BANNER, final_color=DARK["purple"], speed=0.18):
    _init_terminal()

    # Limpa a tela antes de começar
    os.system('cls' if os.name == 'nt' else 'clear')

    # Ajuste fino: remove linhas vazias extras para evitar saltos na animação
    clean_banner = banner_text.strip("\r\n")
    lines = clean_banner.splitlines()
    num_lines = len(lines)

    try:
        for color in ANIM_SEQUENCE:
            # Imprime o banner com a cor atual
            sys.stdout.write(color + clean_banner + DARK["reset"] + "\n")
            sys.stdout.flush()
            time.sleep(speed)

            # Move o cursor de volta para o topo do banner (ANSI Escape)
            sys.stdout.write(f"\033[{num_lines}A")

        # Imprime o banner final para fixar na tela
        sys.stdout.write(final_color + clean_banner + DARK["reset"] + "\n\n")
        sys.stdout.flush()

    except Exception:
        # Fallback caso o terminal não suporte escapes
        print(final_color + clean_banner + DARK["reset"])

if __name__ == "__main__":
    cyber_boot()
    print(f"{DARK['violet']}[+] SHADOWSEC CORE ONLINE{DARK['reset']}\n")
