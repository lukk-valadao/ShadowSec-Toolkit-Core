from core.module_result import ModuleResult, Status, Severity
from core.base_module import BaseModule
from core.module_scope import ModuleScope
from utils.logger import log_json_audit, get_executed_by, get_host_info

import shutil
import subprocess
import platform
from datetime import datetime
from pathlib import Path


class FirewallApply(BaseModule):
    name = "Firewall Hardening (UFW)"
    scope = ModuleScope.DESKTOP_ONLY
    apply_supported = True
    requires_root = True

    def __init__(self, ssh_port: int = 22):
        self.ssh_port = ssh_port

    def run(self) -> ModuleResult:
        system = platform.system().lower()
        changes = []

        # 1️⃣ Só funciona em Linux
        if system != "linux":
            log_json_audit(
                module_name="firewall",
                payload={
                    "module": self.name,
                    "status": Status.NOT_APPLICABLE,
                    "severity": Severity.INFO,
                    "summary": "Firewall hardening supported only on Linux",
                    "executed_by": get_executed_by(),
                    "host": get_host_info(),
                    "platform": system
                }
            )
            return ModuleResult(
                module=self.name,
                status=Status.NOT_APPLICABLE,
                severity=Severity.INFO,
                summary="Firewall hardening supported only on Linux",
                platform=system
            )

        # 2️⃣ Verifica se UFW está instalado
        if not shutil.which("ufw"):
            log_json_audit(
                module_name="firewall",
                payload={
                    "module": self.name,
                    "status": Status.FAIL,
                    "severity": Severity.CRITICAL,
                    "summary": "UFW is not installed",
                    "recommendations": ["Install ufw before applying hardening"],
                    "executed_by": get_executed_by(),
                    "host": get_host_info(),
                    "platform": system
                }
            )
            return ModuleResult(
                module=self.name,
                status=Status.FAIL,
                severity=Severity.CRITICAL,
                summary="UFW is not installed",
                recommendations=["Install ufw before applying hardening"],
                platform=system
            )

        # 3️⃣ Começa a aplicar hardening
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = Path.home() / f"ufw_backup_{timestamp}.txt"

        # Criação de backup
        self._run(f"sudo ufw status numbered > {backup}")
        changes.append(f"Backup created: {backup}")

        # Resetando as regras do UFW
        self._run("sudo ufw --force reset")
        changes.append("Firewall rules reset")

        # Aplicando políticas padrão
        self._run("sudo ufw default deny incoming")
        self._run("sudo ufw default allow outgoing")
        changes.append("Default policies applied")

        # Permitindo portas necessárias
        self._run(f"sudo ufw allow {self.ssh_port}/tcp")
        self._run("sudo ufw allow 80/tcp")
        self._run("sudo ufw allow 443/tcp")
        changes.append("SSH, HTTP and HTTPS allowed")

        # Ativando logging e habilitando firewall
        self._run("sudo ufw logging on")
        self._run("sudo ufw --force enable")
        changes.append("Firewall enabled with logging")

        # 4️⃣ Log JSON de auditoria
        log_json_audit(
            module_name="firewall",
            payload={
                "module": self.name,
                "module_version": "1.0.0",
                "action": "apply",
                "status": Status.OK,
                "severity": Severity.INFO,
                "executed_by": get_executed_by(),
                "host": get_host_info(),
                "platform": system,
                "data": {"ssh_port": self.ssh_port, "changes": changes}
            }
        )

        # 5️⃣ Retorna resultado do módulo
        return ModuleResult(
            module=self.name,
            status=Status.OK,
            severity=Severity.INFO,
            summary="Firewall hardened successfully",
            data={"changes": changes},
            platform=system
        )

    def _run(self, cmd: str):
        """Executa comandos shell"""
        subprocess.run(cmd, shell=True, check=True)
