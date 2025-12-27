import importlib
import pkgutil
import logging # Ou seu utils.logger
from typing import List
from core.base_module import BaseModule

def load_modules(package: str) -> List[BaseModule]:
    """
    Localiza e instancia dinamicamente todos os submódulos que herdam de BaseModule.
    """
    modules = []

    try:
        pkg = importlib.import_module(package)
    except ImportError as e:
        print(f"[!] Erro crítico: Pacote de módulos '{package}' não encontrado. {e}")
        return []

    for _, modname, _ in pkgutil.iter_modules(pkg.__path__):
        full_mod_path = f"{package}.{modname}"

        try:
            # Importa o módulo dinamicamente
            module = importlib.import_module(full_mod_path)

            # Procura por classes que herdam de BaseModule
            for obj in module.__dict__.values():
                if (
                    isinstance(obj, type)
                    and issubclass(obj, BaseModule)
                    and obj is not BaseModule
                ):
                    # Instancia o módulo e adiciona à lista
                    modules.append(obj())

        except Exception as e:
            # Se um módulo falhar, o Core avisa mas continua carregando os outros
            print(f"[!] Aviso: Falha ao carregar o módulo '{full_mod_path}': {e}")
            continue

    return modules
