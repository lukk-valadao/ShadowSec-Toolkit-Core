from enum import Enum


class ModuleScope(Enum):
    DESKTOP_ONLY = "desktop_only"
    SHARED = "shared"
    MOBILE_VIEW = "mobile_view"
