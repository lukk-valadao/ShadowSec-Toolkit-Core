import platform
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

from core.base_module import BaseModule
from core.module_result import ModuleResult, Status, Severity
from core.module_scope import ModuleScope
from utils.logger import log_json_audit, get_executed_by, get_host_info

class FirewallApply(BaseModule):
    name = "Firewall Hardening (UFW)"
    scope = ModuleScope.DESKTOP_ONLY
    apply_supported = True

    def __init__(self, ssh_port: int = 22):
        self.ssh_port = ssh_port

    def run(self) -> ModuleResult:
        system = platform.system().lower()
        changes = []

        # 1. Validação de Plataforma
        if system != "linux":
            return self._finalize(ModuleResult(
                module=self.name,
                status=Status.NOT_APPLICABLE,
                severity=Severity.INFO,
                summary="Firewall hardening supported only on Linux",
                platform=system
            ))

        # 2. Verificação de Dependência
        if not shutil.which("ufw"):
            return self._finalize(ModuleResult(
                module=self.name,
                status=Status.FAIL,
                severity=Severity.CRITICAL,
                summary="UFW is not installed",
                recommendations=["Install ufw before applying hardening"],
                platform=system
            ))

        try:
            # 3. Execução das Ações de Hardening
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup = Path.home() / f"ufw_backup_{timestamp}.txt"

            # Backup usando redirecionamento seguro via shell apenas para o dump de arquivo
            subprocess.run(f"sudo ufw status numbered > {backup}", shell=True, check=True)
            changes.append(f"Backup created: {backup}")

            # Comandos usando Listas (Sem shell=True) para segurança total
            actions = [
                (["sudo", "ufw", "--force", "reset"], "Firewall rules reset"),
                (["sudo", "ufw", "default", "deny", "incoming"], "Default deny incoming applied"),
                (["sudo", "ufw", "default", "allow", "outgoing"], "Default allow outgoing applied"),
                (["sudo", "ufw", "allow", f"{self.ssh_port}/tcp"], f"SSH port {self.ssh_port} allowed"),
                (["sudo", "ufw", "allow", "80/tcp"], "HTTP allowed"),
                (["sudo", "ufw", "allow", "443/tcp"], "HTTPS allowed"),
                (["sudo", "ufw", "logging", "on"], "Logging enabled"),
                (["sudo", "ufw", "--force", "enable"], "Firewall enabled")
            ]

            for cmd, msg in actions:
                subprocess.run(cmd, check=True)
                changes.append(msg)

            result = ModuleResult(
                module=self.name,
                status=Status.OK,
                severity=Severity.INFO,
                summary="Firewall hardened successfully",
                data={"changes": changes},
                platform=system
            )

        except Exception as e:
            result = ModuleResult(
                module=self.name,
                status=Status.FAIL,
                severity=Severity.CRITICAL,
                summary="Failed to apply firewall hardening",
                data={"error": str(e), "changes_made": changes},
                platform=system
            )

        return self._finalize(result)

    def _finalize(self, result: ModuleResult) -> ModuleResult:
        """Centraliza o log de auditoria injetando metadados extras."""
        payload = result.__dict__.copy()
        payload.update({
            "executed_by": get_executed_by(),
            "host": get_host_info(),
            "action": "apply"
        })
        log_json_audit(module_name="firewall", payload=payload)
        return result
