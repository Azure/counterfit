from enum import Enum


class ModelDataType(Enum):
    text = "text"
    image = "image"


class ModelLocation(Enum):
    local = "local"
    remote = "remote"


class AttackFramework(Enum):
    art = "art"
    textattack = "textattack"


class AttackCategory(Enum):
    blackbox = "blackbox"


class AttackTypes(Enum):
    evasion = "evasion"


class AttackStatus(Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
