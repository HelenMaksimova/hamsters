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
    _bonus_damage: int = field(default=0, init=False)
    _bonus_armor: int = field(default=0, init=False)
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
    def current_hp(self) -> int:
        return self._current_hp

    def take_damage(self, damage: int):
        damage -= self.armor
        if damage < 0:
            damage = 0

        self._current_hp -= damage
        if self._current_hp < 0:
            self._current_hp = 0

    def change_base_damage(self, number: int) -> None:
        self._damage += number

        if self._damage < 1:
            self._damage = 1

    def change_base_armor(self, number: int) -> None:
        self._armor += number

        if self._armor < 0:
            self._armor = 0

    def change_bonus_damage(self, number: int) -> None:
        self._bonus_damage += number

        if self._bonus_damage < 0:
            self._bonus_damage = 0

    def change_bonus_armor(self, number: int) -> None:
        self._bonus_armor += number

        if self._bonus_armor < 0:
            self._bonus_armor = 0


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
        if self.current_hp < 0:
            self.current_hp = 0


@dataclass
class NPCharacter:
    name: str
    friendship_score: int = 0