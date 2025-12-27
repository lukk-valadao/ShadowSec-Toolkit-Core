from enum import Enum

class ModuleScope(str, Enum): # Adicionado 'str' para facilitar logs e comparações
    DESKTOP_ONLY = "desktop_only"
    SHARED = "shared"
    MOBILE_VIEW = "mobile_view"
