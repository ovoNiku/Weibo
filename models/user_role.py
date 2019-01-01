import json
from enum import (
    Enum,
    auto,
)


class UserRole(Enum):
    guest = auto()
    normal = auto()


class NikuEncoder(json.JSONEncoder):
    prefix = "__enum__"

    def default(self, o):
        if isinstance(o, UserRole):
            return {self.prefix: o.name}
        else:
            return super().default(o)


def niku_decode(d):
    if NikuEncoder.prefix in d:
        name = d[NikuEncoder.prefix]
        return UserRole[name]
    else:
        return d
