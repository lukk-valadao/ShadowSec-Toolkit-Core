import importlib
import pkgutil
from typing import List, Type

from core.base_module import BaseModule


def load_modules(package: str):
    modules = []
    pkg = importlib.import_module(package)

    for _, modname, _ in pkgutil.iter_modules(pkg.__path__):
        print(f"[DEBUG] importando módulo: {package}.{modname}")
        module = importlib.import_module(f"{package}.{modname}")

        for obj in module.__dict__.values():
            if (
                isinstance(obj, type)
                and issubclass(obj, BaseModule)
                and obj is not BaseModule
            ):
                print(f"[DEBUG] módulo válido encontrado: {obj.__name__}")
                modules.append(obj())

    return modules

