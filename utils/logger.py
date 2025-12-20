# utils/logger.py
import logging
from pathlib import Path
from datetime import datetime
import json
import os
import socket
import getpass
import uuid
import platform



# Diretório padrão de logs do projeto
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_LEVEL = logging.INFO

def log_json_audit(module_name: str, payload: dict):
    """
    Logger de auditoria em JSON (audit log).
    Ideal para relatórios, SIEM e compliance.
    """

    timestamp = datetime.utcnow().isoformat() + "Z"
    audit_file = LOG_DIR / f"shadowsec_audit_{datetime.now().strftime('%Y%m%d')}.log"

    event = {
        "event_id": str(uuid.uuid4()),
        "timestamp": timestamp,
        **payload
    }

    with open(audit_file, "a") as f:
        f.write(json.dumps(event) + "\n")

def get_executed_by():
    return {
        "user": getpass.getuser(),
        "uid": os.getuid(),
        "euid": os.geteuid(),
        "sudo": os.geteuid() == 0
    }


def get_host_info():
    return {
        "hostname": socket.gethostname(),
        "platform": platform.system().lower(),
        "kernel": platform.release()
    }



