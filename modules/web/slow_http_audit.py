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

    # caminho padrão (nginx, pode expandir depois)
    LOG_PATHS = [
        Path("/var/log/nginx/access.log"),
        Path("/var/log/apache2/access.log")
    ]

    # heurísticas seguras
    MAX_REQUEST_TIME = 60        # segundos
    MIN_BYTES = 1024             # 1 KB
    MIN_SUSPECT_REQUESTS = 5

    def run(self) -> ModuleResult:
        log_file = self._find_log_file()

        if not log_file:
            return ModuleResult(
                module=self.name,
                status=Status.NOT_APPLICABLE,
                severity=Severity.INFO,
                summary="No web server access log found",
            )

        suspects = self._analyze_log(log_file)

        if not suspects:
            return ModuleResult(
                module=self.name,
                status=Status.OK,
                severity=Severity.INFO,
                summary="No slow HTTP behavior detected",
            )

        log_json_audit(
            module_name="slow_http_audit",
            payload={
                "module": self.name,
                "status": "warning",
                "severity": "medium",
                "executed_by": get_executed_by(),
                "host": get_host_info(),
                "data": {
                    "suspect_ips": list(suspects.keys()),
                    "details": suspects
                }
            }
        )

        return ModuleResult(
            module=self.name,
            status=Status.OK,
            severity=Severity.MEDIUM,
            summary="Potential slow HTTP behavior detected",
            data={
                "suspect_ips": list(suspects.keys()),
                "details": suspects
            },
            recommendations=[
                "Revisar as configurações de tempo limite de requisição do servidor web",
                "Habilitar a mitigação de requisições lentas (client_body_timeout, RequestReadTimeout)",
                "Monitorar esses IPs para persistência"
            ]
        )

    # --------------------------------------------------

    def _find_log_file(self):
        for path in self.LOG_PATHS:
            if path.exists():
                return path
        return None

    def _analyze_log(self, log_file: Path):
        """
        Analisa logs procurando POSTs longos e lentos
        """
        suspects = defaultdict(lambda: {
            "slow_requests": 0,
            "total_bytes": 0
        })

        # regex genérico (nginx/apache simplificado)
        log_pattern = re.compile(
            r'(?P<ip>\d+\.\d+\.\d+\.\d+).*"POST .*" \d+ (?P<bytes>\d+) .* (?P<time>\d+\.\d+)'
        )

        with log_file.open(errors="ignore") as f:
            for line in f:
                match = log_pattern.search(line)
                if not match:
                    continue

                ip = match.group("ip")
                size = int(match.group("bytes"))
                duration = float(match.group("time"))

                if duration >= self.MAX_REQUEST_TIME and size <= self.MIN_BYTES:
                    suspects[ip]["slow_requests"] += 1
                    suspects[ip]["total_bytes"] += size

        # filtra só IPs relevantes
        return {
            ip: data
            for ip, data in suspects.items()
            if data["slow_requests"] >= self.MIN_SUSPECT_REQUESTS
        }

