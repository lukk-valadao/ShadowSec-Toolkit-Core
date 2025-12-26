#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import platform
import json
from pathlib import Path
from datetime import datetime

from utils.cyber_banner import cyber_boot, DARK
from utils.logger import log_json_audit, get_executed_by, get_host_info
from utils.privileges import require_root

from core.module_loader import load_modules
from core.module_scope import ModuleScope
from core.module_result import ModuleResult

# ==========================================================
# DIRETÓRIO DE LOGS
# ==========================================================
BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# ==========================================================
# AUX CLI
# ==========================================================
def clear():
    os.system("cls" if platform.system() == "Windows" else "clear")

def pause():
    input("\nPressione Enter para continuar...")

def render_result(result: ModuleResult):
    print(f"\n{DARK['blood']}[ {result.module} ]{DARK['reset']}")
    print(f"Status   : {result.status}")
    print(f"Severity : {result.severity}")
    print(f"Resumo   : {result.summary}")

    if result.data:
        print("\nDetalhes:")
        for k, v in result.data.items():
            print(f" - {k}: {v}")

    if result.recommendations:
        print("\nRecomendações:")
        for r in result.recommendations:
            print(f" • {r}")

    # REMOVIDO log_json_audit daqui


# ==========================================================
# MENU
# ==========================================================
def menu():
    modules = load_modules("modules")

    while True:
        clear()
        UNIVERSAL_BANNER = f"""{DARK['blood']}
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
    ╚══════════════════════════════════════════════════════════════╝{DARK['reset']}
"""

        print(UNIVERSAL_BANNER)


        print("[ 0 ] Sair")

        indexed = {}
        idx = 1

        for m in modules:
            if m.scope == ModuleScope.DESKTOP_ONLY:
                print(f"[ {idx} ] {m.name}")
                indexed[str(idx)] = m
                idx += 1

        opt = input("\nEscolha uma opção: ").strip()

        if opt == "0":
            print("Saindo...")
            break

        module = indexed.get(opt)
        if module:
            result = module.run()
            render_result(result)
            pause()
        else:
            print("Opção inválida.")
            pause()

# ==========================================================
# ========================= MAIN ===========================
# ==========================================================
if __name__ == "__main__":
    cyber_boot()
    require_root()
    menu()
