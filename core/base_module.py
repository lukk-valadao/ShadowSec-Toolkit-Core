from abc import ABC, abstractmethod
from core.module_result import ModuleResult
from core.module_scope import ModuleScope


class BaseModule(ABC):
    name: str = "Unnamed Module"
    scope: ModuleScope = ModuleScope.SHARED
    apply_supported: bool = False

    @abstractmethod
    def run(self) -> ModuleResult:
        pass
