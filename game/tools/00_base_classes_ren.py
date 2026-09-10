"""renpy
init -999 python:
"""

from dataclasses import dataclass, asdict, field
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


@dataclass
class Mob:
    name: str
    current_health: int = 0
    max_health: int = 0

    def restore(self) -> None:
        self.current_health = self.max_health

    def defeat(self) -> None:
        self.current_health = 0

    def take_damage(self, damage: int = 1) -> None:
        self.current_health -= damage
        if self.current_health < 0:
            self.current_health = 0


@dataclass
class ButtleData:
    active_mobs: set[str] = field(default_factory=set)
    defeated_mobs: set[str] = field(default_factory=set)

    def defeat(self, mob: Mob | str) -> None:
        name = mob.name if isinstance(mob, Mob) else mob
        if name in self.active_mobs:
            self.active_mobs.remove(name)
            self.defeated_mobs.add(name)

    def is_defeated(self, mob: Mob | str) -> bool:
        name = mob.name if isinstance(mob, Mob) else mob

        return name in self.defeated_mobs

    def is_active(self, mob: Mob | str) -> bool:
        name = mob.name if isinstance(mob, Mob) else mob
        return name in self.active_mobs

    def add_to_buttle(self, *mobs: Mob | str) -> None:
        names = {mob.name if isinstance(mob, Mob) else mob for mob in mobs}
        self.active_mobs.update(names)

    def remove_from_buttle(self, *mobs: Mob | str) -> None:
        names = {mob.name if isinstance(mob, Mob) else mob for mob in mobs}
        self.active_mobs.difference_update(names)
        self.defeated_mobs.difference_update(names)
