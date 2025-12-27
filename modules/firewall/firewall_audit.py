import platform
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

from core.base_module import BaseModule
from core.module_result import ModuleResult, Status, Severity
from core.module_scope import ModuleScope
from utils.logger import log_json_audit

class FirewallAudit(BaseModule):
    name = "Firewall Audit (UFW)"
    scope = ModuleScope.DESKTOP_ONLY
    apply_supported = True

    def run(self) -> ModuleResult:
        """
        Executa a auditoria do firewall UFW no Linux.
        """
        system = platform.system().lower()

        # 1. Verificação de Sistema Operacional
        if system != "linux":
            result = ModuleResult(
                module=self.name,
                status=Status.NOT_APPLICABLE,
                severity=Severity.INFO,
                summary="Auditoria de firewall (UFW) suportada apenas em sistemas Linux.",
                platform=system
            )
            return self._finalize_audit(result)

        # 2. Verificação de Dependência (Se o binário existe)
        if not shutil.which("ufw"):
            result = ModuleResult(
                module=self.name,
                status=Status.FAIL,
                severity=Severity.HIGH,
                summary="Utilitário UFW não encontrado no sistema.",
                recommendations=["Instale o ufw (sudo apt install ufw) para proteger o sistema."],
                platform=system
            )
            return self._finalize_audit(result)

        # 3. Execução do Comando e Coleta de Dados
        try:
            # Uso seguro de lista sem shell=True para evitar Command Injection
            proc = subprocess.run(
                ["ufw", "status", "verbose"],
                capture_output=True,
                text=True,
                check=False  # Não levanta exceção se o retorno não for zero
            )

            output = proc.stdout.strip()
            is_active = "Status: active" in output

            result = ModuleResult(
                module=self.name,
                status=Status.OK if is_active else Status.FAIL,
                severity=Severity.INFO if is_active else Severity.HIGH,
                summary="O Firewall está ativo e protegendo o sistema." if is_active else "O Firewall está instalado, mas encontra-se DESATIVADO.",
                data={"ufw_raw_output": output},
                recommendations=[] if is_active else ["Ative o firewall usando o módulo de 'apply' ou 'sudo ufw enable'"],
                platform=system
            )

        except Exception as e:
            # Tratamento de erro genérico para evitar crash do Core
            result = ModuleResult(
                module=self.name,
                status=Status.FAIL,
                severity=Severity.CRITICAL,
                summary="Falha interna ao tentar auditar o firewall.",
                data={"error_details": str(e)},
                platform=system
            )

        return self._finalize_audit(result)

    def _finalize_audit(self, result: ModuleResult) -> ModuleResult:
        """
        Método auxiliar para centralizar o log de auditoria antes de retornar o resultado.
        """
        # Garante que o payload seja uma string/dict serializável
        log_json_audit(module_name=self.name, payload=result.__dict__)
        return result
