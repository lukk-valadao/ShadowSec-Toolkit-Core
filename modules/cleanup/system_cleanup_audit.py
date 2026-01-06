import platform
import subprocess
import shutil
from pathlib import Path

from core.base_module import BaseModule
from core.module_result import ModuleResult, Status, Severity
from core.module_scope import ModuleScope
from utils.logger import log_json_audit, get_executed_by, get_host_info


class SystemCleanupAudit(BaseModule):
    name = "System Cleanup Audit"
    scope = ModuleScope.DESKTOP_ONLY
    apply_supported = False
    requires_root = False

    def run(self) -> ModuleResult:
        system = platform.system().lower()

        # 1️⃣ Apenas Linux (por enquanto)
        if system != "linux":
            result = ModuleResult(
                module=self.name,
                status=Status.NOT_APPLICABLE,
                severity=Severity.INFO,
                summary="System cleanup audit supported only on Linux",
                platform=system
            )
            log_json_audit(self.name, result.__dict__)
            return result

        data = {}

        try:
            # 2️⃣ Pacotes órfãos (apt autoremove --dry-run)
            if shutil.which("apt"):
                proc = subprocess.run(
                    ["apt", "autoremove", "--dry-run"],
                    capture_output=True,
                    text=True
                )
                orphan_packages = [
                    line.strip()
                    for line in proc.stdout.splitlines()
                    if line.startswith("Remv ")
                ]
                data["orphan_packages_count"] = len(orphan_packages)
            else:
                data["orphan_packages_count"] = None

            # 3️⃣ Cache do APT
            apt_cache = Path("/var/cache/apt/archives")
            if apt_cache.exists():
                cache_size = sum(
                    f.stat().st_size for f in apt_cache.glob("*.deb") if f.is_file()
                )
                data["apt_cache_mb"] = round(cache_size / (1024 * 1024), 2)
            else:
                data["apt_cache_mb"] = None

            # 4️⃣ Logs do systemd journal
            proc = subprocess.run(
                ["journalctl", "--disk-usage"],
                capture_output=True,
                text=True
            )
            journal_size = None
            for line in proc.stdout.splitlines():
                if "used" in line:
                    journal_size = line.strip()
                    break
            data["journal_disk_usage"] = journal_size

            # 5️⃣ Lixeira do usuário
            trash_dir = Path.home() / ".local/share/Trash/files"
            if trash_dir.exists():
                trash_size = sum(
                    f.stat().st_size for f in trash_dir.rglob("*") if f.is_file()
                )
                data["trash_mb"] = round(trash_size / (1024 * 1024), 2)
            else:
                data["trash_mb"] = 0

            # 6️⃣ Avaliação simples
            cleanup_needed = any(
                [
                    data.get("orphan_packages_count", 0) > 0,
                    data.get("apt_cache_mb", 0) > 100,
                    data.get("trash_mb", 0) > 0,
                ]
            )

            status = Status.WARNING if cleanup_needed else Status.OK
            summary = (
                "System cleanup recommended"
                if cleanup_needed
                else "No significant cleanup needed"
            )

            result = ModuleResult(
                module=self.name,
                status=status,
                severity=Severity.INFO,
                summary=summary,
                data=data,
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
                    "data": data,
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
                summary="System cleanup audit failed",
                data={"error": str(e)},
                platform=system
            )
            log_json_audit(self.name, result.__dict__)
            return result

