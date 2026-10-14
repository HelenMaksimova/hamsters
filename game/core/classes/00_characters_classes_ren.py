"""renpy
init -998 python:
"""

from dataclasses import dataclass, field


@dataclass
class Ability:
    title: str
    icon: str
    image: str
    description: str | None = None

    def use(self):
        pass


@dataclass
class Player:
    _abilities: list[Ability] = field(default_factory=list, init=False)
    _current_hp: int = field(default=0, init=False)
    _damage: int = field(default=1, init=False)
    _armor: int = field(default=0, init=False)
    _heal: int = field(default=1, init=False)
    _bonus_damage: int = field(default=0, init=False)
    _bonus_armor: int = field(default=0, init=False)
    _bonus_heal: int = field(default=0, init=False)
    max_hp: int
    battle_icon: str

    def __post_init__(self):
        self._current_hp = self.max_hp

    @property
    def abilities(self) -> list[Ability]:
        return self._abilities

    @property
    def armor(self) -> int:
        return self._armor + self._bonus_armor

    @property
    def damage(self) -> int:
        return self._damage + self._bonus_damage

    @property
    def heal(self) -> int:
        return self._heal + self._bonus_heal

    @property
    def current_hp(self) -> int:
        return self._current_hp

    def restore_health(self, full: bool = False):
        self._current_hp += self.heal
        if self._current_hp > self.max_hp or full:
            self._current_hp = self.max_hp

    def take_damage(self, damage: int):
        damage -= self.armor
        damage = max(damage, 0)

        self._current_hp -= damage
        self._current_hp = max(self._current_hp, 0)

    def change_base_damage(self, number: int) -> None:
        self._damage += number
        self._damage = max(self._damage, 1)

    def change_base_armor(self, number: int) -> None:
        self._armor += number
        self._armor = max(self._armor, 0)

    def change_base_heal(self, number: int) -> None:
        self._heal += number
        self._heal = max(self._heal, 1)

    def change_bonus_damage(self, number: int) -> None:
        self._bonus_damage += number
        self._bonus_damage = max(self._bonus_damage, 0)

    def change_bonus_armor(self, number: int) -> None:
        self._bonus_armor += number
        self._bonus_armor = max(self._bonus_armor, 0)

    def change_bonus_heal(self, number: int) -> None:
        self._bonus_heal += number
        self._bonus_heal = max(self._bonus_heal, 0)


@dataclass
class Mob:
    name: str
    max_hp: int
    battle_icon: str
    current_hp: int = 0
    damage: int = 1

    def __post_init__(self):
        self.current_hp = self.max_hp

    def take_damage(self, damage: int):
        self.current_hp -= damage
        self.current_hp = max(self.current_hp, 0)


@dataclass
class NPCharacter:
    name: str
    _friendship_score: int = field(default=0, init=False)

    @property
    def friendship_score(self) -> int:
        return self._friendship_score

    def change_friendship_score(self, number: int) -> None:
        self._friendship_score += number
        self._friendship_score = max(self._friendship_score, 0)
