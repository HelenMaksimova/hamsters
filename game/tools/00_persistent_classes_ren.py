"""renpy
init -999 python:
"""

from dataclasses import asdict, dataclass, field
from typing import Self


@dataclass
class BasePersistentData:
    _key: str = field(repr=False)

    @property
    def key(self) -> str:
        if not self._key:
            raise ValueError("Key is not defined")

        return self._key

    def save(self) -> None:
        data = asdict(self)
        data.pop("_key")

        setattr(persistent, self.key, data)
        renpy.save_persistent()

    @classmethod
    def load(cls, key: str, **default) -> Self:
        data = getattr(persistent, key, None) or default

        data.pop("_key", None)
        return cls(key, **data)
