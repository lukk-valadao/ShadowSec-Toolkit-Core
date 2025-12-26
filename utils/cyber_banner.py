# ================================================
# ANIMATED BANNER ENGINE – Universal Cyberpunk v1
# Cole esse bloco no topo de qualquer script
# ================================================

import os
import time
import sys

# PALETA DARK CYBERPUNK (mude à vontade)
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

# Sequência da animação (só roda uma vez)
ANIM_SEQUENCE = [
    DARK["purple"], DARK["blood"], DARK["violet"],
    DARK["midnight"], DARK["magenta"], DARK["orchid"],
    DARK["cyan"], DARK["purple"]
]

# Seu banner aqui (pode ter quantas linhas quiser)
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
    ║ ▓▓        システム侵入検知モードが有効になりました        ▓▓ ║
    ║ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ║
    ╚══════════════════════════════════════════════════════════════╝
"""

def cyber_boot(banner_text=UNIVERSAL_BANNER, final_color=DARK["purple"], speed=0.22):
    os.system('cls' if os.name == 'nt' else 'clear')

    # Contar linhas corretamente (incluindo a última mesmo sem \n final)
    num_lines = banner_text.count('\n') + 1

    for color in ANIM_SEQUENCE:
        print(color + banner_text + DARK["reset"])
        time.sleep(speed)
        print(f"\033[{num_lines}A", end="")

    # Banner final
    print(final_color + banner_text + DARK["reset"])
    time.sleep(0.8)

# ================================================
# EXEMPLO DE USO EM QUALQUER PROJETO
# ================================================

if __name__ == "__main__":
    # Só mudar o texto aqui ou passar como parâmetro
    cyber_boot()                                      # usa o banner padrão
    # cyber_boot(meu_banner_personalizado)            # usa banner customizado
    # cyber_boot(final_color=DARK["blood"], speed=0.15)  # cor final vermelha + mais rápido

    print(f"{DARK['violet']}[+] O modo de detecção de intrusão do sistema está ativado.{DARK['reset']}\n")
