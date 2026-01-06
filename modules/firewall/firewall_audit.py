import platform
import subprocess
import shutil
from core.module_result import ModuleResult, Status, Severity
from core.module_scope import ModuleScope
import shutil
import subprocess
import platform
from datetime import datetime
from pathlib import Path
from core.base_module import BaseModule, ModuleScope
from utils.logger import log_json_audit, get_executed_by, get_host_info


class FirewallAudit(BaseModule):
    name = "Firewall Audit (UFW)"
    scope = ModuleScope.DESKTOP_ONLY
    apply_supported = True
    requires_root = False


    def run(self) -> ModuleResult:
        system = platform.system().lower()

        # Só funciona em Linux
        if system != "linux":
            result = ModuleResult(
                module=self.name,
                status=Status.NOT_APPLICABLE,
                severity=Severity.INFO,
                summary="Firewall audit supported only on Linux",
                platform=system
            )
            log_json_audit(module_name=self.name, payload=result.__dict__)
            return result

        # Verifica se UFW está instalado
        if not shutil.which("ufw"):
            result = ModuleResult(
                module=self.name,
                status=Status.FAIL,
                severity=Severity.HIGH,
                summary="UFW is not installed",
                recommendations=["Install ufw to enable firewall protection"],
                platform=system
            )
            log_json_audit(module_name=self.name, payload=result.__dict__)
            return result

        try:
            proc = subprocess.run(
                ["ufw", "status", "verbose"],
                capture_output=True,
                text=True
            )

            output = proc.stdout.strip()

            if "Status: active" in output:
                status = Status.OK
                severity = Severity.INFO
                summary = "Firewall is active"
            else:
                status = Status.FAIL
                severity = Severity.HIGH
                summary = "Firewall is installed but inactive"

            result = ModuleResult(
                module=self.name,
                status=status,
                severity=severity,
                summary=summary,
                data={"ufw_status": output},
                platform=system
            )
            log_json_audit(module_name=self.name, payload=result.__dict__)
            return result

        except Exception as e:
            result = ModuleResult(
                module=self.name,
                status=Status.FAIL,
                severity=Severity.CRITICAL,
                summary="Firewall audit failed",
                data={"error": str(e)},
                platform=system
            )
            log_json_audit(module_name=self.name, payload=result.__dict__)
            return result
