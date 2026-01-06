import platform
import subprocess
import shutil
from datetime import datetime

from core.base_module import BaseModule
from core.module_result import ModuleResult, Status, Severity
from core.module_scope import ModuleScope
from utils.logger import log_json_audit, get_executed_by, get_host_info


class SystemUpdatesApply(BaseModule):
    name = "System Updates Apply (APT)"
    scope = ModuleScope.DESKTOP_ONLY
    apply_supported = True
    requires_root = True

    def __init__(self, full_upgrade: bool = False):
        """
        :param full_upgrade: Se True, executa apt full-upgrade.
                             Caso contrário, usa apt upgrade.
        """
        self.full_upgrade = full_upgrade

    def run(self) -> ModuleResult:
        system = platform.system().lower()
        changes = []

        # 1️⃣ Apenas Linux
        if system != "linux":
            result = ModuleResult(
                module=self.name,
                status=Status.NOT_APPLICABLE,
                severity=Severity.INFO,
                summary="System updates apply supported only on Linux",
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
            # 3️⃣ apt update
            subprocess.run(
                ["sudo", "apt", "update"],
                check=True,
                capture_output=True,
                text=True
            )
            changes.append("apt update executed")

            # 4️⃣ Escolha do modo de upgrade
            if self.full_upgrade:
                upgrade_cmd = ["sudo", "apt", "full-upgrade", "-y"]
                upgrade_mode = "full-upgrade"
            else:
                upgrade_cmd = ["sudo", "apt", "upgrade", "-y"]
                upgrade_mode = "upgrade"

            proc = subprocess.run(
                upgrade_cmd,
                capture_output=True,
                text=True
            )

            output = proc.stdout + proc.stderr

            # 5️⃣ Extração simples de pacotes atualizados
            updated_packages = []
            for line in output.splitlines():
                if line.startswith("Preparing to unpack") or line.startswith("Unpacking"):
                    parts = line.split()
                    if len(parts) >= 3:
                        updated_packages.append(parts[-1])

            if proc.returncode != 0:
                raise RuntimeError("APT upgrade failed")

            changes.append(f"apt {upgrade_mode} executed")

            result = ModuleResult(
                module=self.name,
                status=Status.OK,
                severity=Severity.INFO,
                summary="System updates applied successfully",
                data={
                    "upgrade_mode": upgrade_mode,
                    "updated_packages": list(set(updated_packages))
                },
                platform=system
            )

            log_json_audit(
                module_name=self.name,
                payload={
                    "module": self.name,
                    "action": "apply",
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
                summary="System updates apply failed",
                data={"error": str(e)},
                platform=system
            )
            log_json_audit(self.name, result.__dict__)
            return result
