import os
import subprocess
import platform
from datetime import datetime
from pathlib import Path

from core.base_module import BaseModule
from core.module_result import ModuleResult, Status, Severity
from core.module_scope import ModuleScope
from utils.logger import log_json_audit, get_executed_by, get_host_info


class SystemCleanupApply(BaseModule):
    name = "System Cleanup Apply"
    scope = ModuleScope.DESKTOP_ONLY
    apply_supported = True
    requires_root = True

    def run(self) -> ModuleResult:
        system = platform.system().lower()
        changes = []
        warnings = []

        # 1️⃣ Apenas Linux
        if system != "linux":
            return ModuleResult(
                module=self.name,
                status=Status.NOT_APPLICABLE,
                severity=Severity.INFO,
                summary="System cleanup apply supported only on Linux",
                platform=system
            )

        # 2️⃣ Usuário real (quem chamou sudo)
        target_user = os.environ.get("SUDO_USER")
        if not target_user:
            target_user = "root"
            warnings.append("SUDO_USER not set, defaulting to root")

        user_home = Path("/home") / target_user

        # 3️⃣ Backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = Path("/root") / f"shadowsec_cleanup_backup_{timestamp}"
        backup_dir.mkdir(parents=True, exist_ok=True)

        # 4️⃣ Snapshot do journal
        journal_snapshot = backup_dir / "journal_usage.txt"
        subprocess.run(
            f"journalctl --disk-usage > {journal_snapshot}",
            shell=True,
            check=False
        )
        changes.append(f"Journal usage snapshot saved: {journal_snapshot}")

        # 5️⃣ Limpeza APT
        subprocess.run("apt autoremove -y", shell=True, check=False)
        changes.append("Unused packages removed (apt autoremove)")

        subprocess.run("apt autoclean -y", shell=True, check=False)
        changes.append("APT cache cleaned (apt autoclean)")

        # 6️⃣ Limpeza do journal
        subprocess.run("journalctl --vacuum-time=5d", shell=True, check=False)
        changes.append("Systemd journal vacuumed (5 days)")

        # 7️⃣ Limpeza REAL da lixeira
        trash_cleaned = False

        # 7.1 Método correto para desktop (gio)
        gio_cmd = (
            f"sudo -u {target_user} "
            f"gio trash --empty"
        )

        gio_result = subprocess.run(gio_cmd, shell=True)

        if gio_result.returncode == 0:
            changes.append("User trash emptied via gio")
            trash_cleaned = True
        else:
            warnings.append("gio trash failed, using fallback cleanup")

        # 7.2 Fallback manual
        if not trash_cleaned:
            trash_paths = [
                user_home / ".local/share/Trash"
            ]

            for base in ["/media", "/run/media"]:
                base_path = Path(base) / target_user
                if base_path.exists():
                    trash_paths.append(base_path)

            for path in trash_paths:
                if path.exists():
                    subprocess.run(
                        f"rm -rf {path}/Trash/* {path}/.Trash-*",
                        shell=True,
                        check=False
                    )

            changes.append("Fallback trash cleanup executed")

        # 8️⃣ Log de auditoria
        log_json_audit(
            module_name="cleanup",
            payload={
                "module": self.name,
                "module_version": "1.1.1",
                "action": "apply",
                "status": Status.OK,
                "severity": Severity.INFO,
                "executed_by": get_executed_by(),
                "host": get_host_info(),
                "platform": system,
                "data": {
                    "target_user": target_user,
                    "backup_dir": str(backup_dir),
                    "changes": changes,
                    "warnings": warnings
                }
            }
        )

        # 9️⃣ Resultado final
        return ModuleResult(
            module=self.name,
            status=Status.OK,
            severity=Severity.INFO,
            summary="System cleanup applied successfully",
            data={
                "target_user": target_user,
                "changes": changes,
                "warnings": warnings
            },
            platform=system
        )
