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

