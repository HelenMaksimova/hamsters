"""renpy
init -999 python:
"""
from dataclasses import dataclass, asdict, field
from typing import Self, Literal
from random import shuffle, sample


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
class BattleData:
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

    def add_to_battle(self, *mobs: Mob | str) -> None:
        names = {mob.name if isinstance(mob, Mob) else mob for mob in mobs}
        self.active_mobs.update(names)

    def remove_from_battle(self, *mobs: Mob | str) -> None:
        names = {mob.name if isinstance(mob, Mob) else mob for mob in mobs}
        self.active_mobs.difference_update(names)
        self.defeated_mobs.difference_update(names)


@dataclass
class BattleCard:
    value: int
    image: str
    position: int | None = None
    state: Literal["closed", "opened", "matched"] = "closed"


@dataclass
class BattleGround:
    _cards: list[BattleCard] = field(default_factory=list, init=False)
    _images_map: dict[int, str] = field(default_factory=dict, init=False)
    _current_card: BattleCard | None = field(default=None, init=False)
    _game_count: int = field(default=0, init=False)
    pending_close: bool = field(default=False, init=False)
    card_values: tuple[int, ...]
    card_images: tuple[str, ...]
    clickable_states: set[str] = field(default_factory=lambda: {"closed",})
    rows_number: int = 2
    columns_number: int = 2

    def __post_init__(self):
        if self.columns_number <= 0 or self.rows_number <=0:
            raise ValueError("The number of rows and columns must be greater than 0")
        elif self.cards_number % 2:
            raise ValueError("The number of cards must be even")
        elif len(self.card_values) * 2 > self.cards_number:
            raise ValueError("The double number of card values must be less than or equal to number of cards")
        elif len(self.card_images) != len(self.card_values):
            raise ValueError("The number of card images must be equal to number of card values")

        self._set_images_map()
        self._create_cards()
        self._set_game_count()

    @property
    def cards_number(self) -> int:
        return self.rows_number * self.columns_number

    @property
    def cards(self) -> list[BattleCard]:
        return self._cards

    @property
    def game_count(self) -> int:
        return self._game_count

    @property
    def is_victory(self) -> bool:
        return self.game_count <= 0

    @property
    def current_card(self) -> BattleCard | None:
        return self._current_card

    def set_current_card(self, position: int) -> None:
        self._current_card = self._cards[position]

    def clear_current_card(self) -> None:
        self._current_card = None

    @property
    def images_map(self) -> dict[int, str]:
        return self._images_map

    def _set_game_count(self) -> None:
        self._game_count = self.cards_number // 2

    def _set_images_map(self) -> None:
        self._images_map = dict(zip(self.card_values, self.card_images))

    def _create_cards(self) -> None:
        rest_number = self.cards_number // 2 % len(self.card_values)
        cycle_number = self.cards_number // 2 // len(self.card_values)

        for _ in range(cycle_number):
            for value, image in self.images_map.items():
                self._cards.extend((BattleCard(value, image), BattleCard(value, image)))

        for value in sample(self.card_values, k=rest_number):
            self._cards.extend((BattleCard(value, self.images_map[value]), BattleCard(value, self.images_map[value])))

        shuffle(self._cards)

        for idx in range(len(self._cards)):
            self._cards[idx].position = idx

    def flip_card(self, position: int) -> None:
        flipped_card = self._cards[position]

        if flipped_card.state in self.clickable_states:
            flipped_card.state = "opened"

            if not self.current_card:
                self.set_current_card(position)
            elif self.current_card.value == flipped_card.value:
                self.current_card.state = "matched"
                flipped_card.state = "matched"
                self._game_count -= 1
                self.clear_current_card()
            else:
                self.pending_close = True
                self.clear_current_card()

    def close_pending(self) -> None:
        if self.pending_close:
            for card in self.cards:
                if card.state == "opened":
                    card.state = "closed"
            self.pending_close = False

    def check_victory(self, label: str) -> None:
        if self.is_victory:
            renpy.jump(label)
