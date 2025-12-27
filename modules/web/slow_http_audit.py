import re
from collections import defaultdict
from pathlib import Path

from core.base_module import BaseModule
from core.module_result import ModuleResult, Status, Severity
from core.module_scope import ModuleScope
from utils.logger import log_json_audit, get_executed_by, get_host_info

class SlowHttpAudit(BaseModule):
    name = "Slow HTTP Audit (RUDY-like)"
    scope = ModuleScope.DESKTOP_ONLY
    apply_supported = False

    LOG_PATHS = [
        Path("/var/log/nginx/access.log"),
        Path("/var/log/apache2/access.log")
    ]

    MAX_REQUEST_TIME = 60.0
    MIN_BYTES = 1024
    MIN_SUSPECT_REQUESTS = 5

    def run(self) -> ModuleResult:
        system_info = get_host_info() # Pega info uma vez para performance
        log_file = self._find_log_file()

        # 1. Caso não encontre logs
        if not log_file:
            result = ModuleResult(
                module=self.name,
                status=Status.NOT_APPLICABLE,
                severity=Severity.INFO,
                summary="No web server access logs found for analysis.",
            )
            return self._finalize(result)

        # 2. Análise dos Logs
        try:
            suspects = self._analyze_log(log_file)

            if not suspects:
                result = ModuleResult(
                    module=self.name,
                    status=Status.OK,
                    severity=Severity.INFO,
                    summary="No slow HTTP behavior detected in recent logs.",
                )
            else:
                result = ModuleResult(
                    module=self.name,
                    status=Status.WARNING, # Alterado para Warning para destacar
                    severity=Severity.MEDIUM,
                    summary=f"Potential slow HTTP behavior detected from {len(suspects)} IPs",
                    data={"suspect_ips": list(suspects.keys()), "details": suspects},
                    recommendations=[
                        "Review web server timeout settings (client_body_timeout, RequestReadTimeout)",
                        "Check for R.U.D.Y or Slowloris attack patterns",
                        "Consider rate-limiting the identified suspect IPs"
                    ]
                )

        except Exception as e:
            result = ModuleResult(
                module=self.name,
                status=Status.FAIL,
                severity=Severity.HIGH,
                summary="Internal error during log analysis",
                data={"error": str(e)}
            )

        return self._finalize(result)

    def _find_log_file(self):
        return next((path for path in self.LOG_PATHS if path.exists()), None)

    def _analyze_log(self, log_file: Path):
        suspects = defaultdict(lambda: {"slow_requests": 0, "total_bytes": 0})

        # Regex mais robusta para tratar variações de logs
        log_pattern = re.compile(
            r'(?P<ip>\d+\.\d+\.\d+\.\d+).*"POST .*" \d+ (?P<bytes>\d+) .* (?P<time>\d+\.\d+)'
        )

        with log_file.open(errors="ignore") as f:
            # Lukk, aqui processamos linha a linha para não estourar a RAM
            for line in f:
                match = log_pattern.search(line)
                if not match:
                    continue

                try:
                    ip = match.group("ip")
                    size = int(match.group("bytes"))
                    duration = float(match.group("time"))

                    if duration >= self.MAX_REQUEST_TIME and size <= self.MIN_BYTES:
                        suspects[ip]["slow_requests"] += 1
                        suspects[ip]["total_bytes"] += size
                except (ValueError, TypeError):
                    continue # Pula linhas com dados de tempo/tamanho corrompidos

        return {
            ip: data for ip, data in suspects.items()
            if data["slow_requests"] >= self.MIN_SUSPECT_REQUESTS
        }

    def _finalize(self, result: ModuleResult) -> ModuleResult:
        """Centraliza o log de auditoria garantindo que SEMPRE grave algo."""
        payload = result.__dict__.copy()
        payload.update({
            "executed_by": get_executed_by(),
            "host": get_host_info(),
            "target_log": str(self._find_log_file() or "None")
        })
        # Aqui ele grava o log independente do resultado (OK, FAIL ou WARNING)
        log_json_audit(module_name="slow_http", payload=payload)
        return result
