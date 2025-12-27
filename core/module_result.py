from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

class Severity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Status(str, Enum):
    OK = "ok"
    WARNING = "warning"
    FAIL = "fail"
    NOT_APPLICABLE = "not_applicable"

@dataclass
class ModuleResult:
    module: str
    status: Status
    severity: Severity
    summary: str

    data: Dict = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    platform: Optional[str] = None

    def __post_init__(self):
        """
        Validação pós-instanciação para garantir que os dados
        recebidos dos módulos sigam o contrato do Core.
        """
        # Garante que, se o módulo passou uma string em vez do Enum,
        # tentamos converter ou validar para evitar erros de tipo adiante.
        if not isinstance(self.status, Status):
            try:
                self.status = Status(self.status)
            except ValueError:
                # Se o status for inválido, força FAIL para segurança
                self.status = Status.FAIL

        if not isinstance(self.severity, Severity):
            try:
                self.severity = Severity(self.severity)
            except ValueError:
                self.severity = Severity.INFO
