import os
import socket
import getpass
import uuid
import platform
import json
from pathlib import Path
from datetime import datetime

# Diretório padrão de logs
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

def log_json_audit(module_name: str, payload: dict):
    """
    Logger de auditoria em JSON com tratamento de erros de serialização.
    """
    try:
        timestamp = datetime.utcnow().isoformat() + "Z"
        audit_file = LOG_DIR / f"shadowsec_audit_{datetime.now().strftime('%Y%m%d')}.log"

        event = {
            "event_id": str(uuid.uuid4()),
            "timestamp": timestamp,
            "module_tag": module_name, # Tag extra para facilitar filtros no SIEM
            **payload
        }

        # Hardening: O parâmetro 'default=str' converte Enums e outros objetos em string
        # automaticamente, evitando que o json.dumps quebre o programa.
        log_line = json.dumps(event, default=str)

        with open(audit_file, "a", encoding="utf-8") as f:
            f.write(log_line + "\n")

    except Exception as e:
        # Se o log falhar, imprimimos um alerta para não perder a informação
        print(f"[!] Erro crítico ao gravar log de auditoria: {e}")

def get_executed_by():
    """Coleta informações de privilégio do usuário atual."""
    try:
        return {
            "user": getpass.getuser(),
            "uid": os.getuid() if hasattr(os, 'getuid') else "N/A",
            "euid": os.geteuid() if hasattr(os, 'geteuid') else "N/A",
            "sudo": (os.geteuid() == 0) if hasattr(os, 'geteuid') else False
        }
    except Exception:
        return {"error": "Could not retrieve user info"}

def get_host_info():
    """Coleta metadados do host para contexto de segurança."""
    return {
        "hostname": socket.gethostname(),
        "platform": platform.system().lower(),
        "kernel": platform.release(),
        "arch": platform.machine()
    }
