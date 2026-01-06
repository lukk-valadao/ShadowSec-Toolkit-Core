import platform
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

from core.base_module import BaseModule
from core.module_result import ModuleResult, Status, Severity
from core.module_scope import ModuleScope
from utils.logger import log_json_audit, get_executed_by, get_host_info


class SystemUpdatesAudit(BaseModule):
    name = "System Updates Audit (APT)"
    scope = ModuleScope.DESKTOP_ONLY
    apply_supported = True
    requires_root = False

    def run(self) -> ModuleResult:
        system = platform.system().lower()
        changes = []

        # 1️⃣ Apenas Linux
        if system != "linux":
            result = ModuleResult(
                module=self.name,
                status=Status.NOT_APPLICABLE,
                severity=Severity.INFO,
                summary="System updates supported only on Linux",
                platform=system
            )
            log_json_audit(self.name, result.__dict__)
            return result

        # 2️⃣ Verifica apt
        if not shutil.which("apt"):
            result = ModuleResult(
                module=self.name,
                status=Status.FAIL,
                severity=Severity.CRITICAL,
                summary="APT package manager not found",
                recommendations=["Ensure this system uses APT-based package management"],
                platform=system
            )
            log_json_audit(self.name, result.__dict__)
            return result

        try:
            # 3️⃣ Executa apt update
            proc = subprocess.run(
                ["sudo", "apt", "update"],
                capture_output=True,
                text=True
            )

            update_output = proc.stdout + proc.stderr

            # Detecta erros comuns de repositório
            repo_errors = []
            for line in update_output.splitlines():
                if "Release file" in line or "404" in line:
                    repo_errors.append(line.strip())

            if repo_errors:
                severity = Severity.HIGH
                changes.append("Repository errors detected during apt update")
            else:
                severity = Severity.INFO

            # 4️⃣ Conta pacotes atualizáveis
            proc_up = subprocess.run(
                ["apt", "list", "--upgradable"],
                capture_output=True,
                text=True
            )

            upgradable = [
                line.split("/")[0]
                for line in proc_up.stdout.splitlines()
                if "upgradable" in line
            ]

            updates_count = len(upgradable)

            if updates_count == 0:
                status = Status.OK
                summary = "System is fully up to date"
            else:
                status = Status.WARNING
                summary = f"{updates_count} packages available for update"

            result = ModuleResult(
                module=self.name,
                status=status,
                severity=severity,
                summary=summary,
                data={
                    "updates_available": updates_count,
                    "packages": upgradable,
                    "repository_errors": repo_errors
                },
                platform=system
            )

            log_json_audit(
                module_name=self.name,
                payload={
                    "module": self.name,
                    "action": "audit",
                    "executed_by": get_executed_by(),
                    "host": get_host_info(),
                    "platform": system,
                    "data": result.data,
                    "status": result.status,
                    "severity": result.severity
                }
            )

            return result

        except Exception as e:
            result = ModuleResult(
                module=self.name,
                status=Status.FAIL,
                severity=Severity.CRITICAL,
                summary="System update audit failed",
                data={"error": str(e)},
                platform=system
            )
            log_json_audit(self.name, result.__dict__)
            return result
