"""renpy
init -996 python:
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from random import sample, shuffle
from typing import Literal


def heal(player: Player, mob: Mob) -> None:
    player.restore_health()


def defence(player: Player, mob: Mob) -> None:
    player.change_bonus_armor(1)


def hit(player: Player, mob: Mob) -> None:
    mob.take_damage(player.damage)


CARDS_MAP = {
    0: ("battle/battle_value_0.png", defence),
    1: ("battle/battle_value_1.png", hit),
    2: ("battle/battle_value_2.png", heal),
}


@dataclass
class BattleCard:
    value: int
    image: str
    action: Callable
    position: int | None = None
    state: Literal["closed", "opened", "matched"] = "closed"


@dataclass
class BattleGround:
    _cards: list[BattleCard] = field(default_factory=list, init=False)
    _current_card: BattleCard | None = field(default=None, init=False)
    _matched_count: int = field(default=0, init=False)
    pending_close: bool = field(default=False, init=False)
    pending_recreate: bool = field(default=False, init=False)
    card_values: tuple[int, ...]
    mob: Mob
    player: Player
    clickable_states: set[str] = field(
        default_factory=lambda: {
            "closed",
        }
    )
    rows_number: int = 2
    columns_number: int = 2

    def __post_init__(self):
        if self.columns_number <= 0 or self.rows_number <= 0:
            raise ValueError(
                "The number of rows and columns must be greater than 0"
            )
        elif self.cards_number % 2:
            raise ValueError("The number of cards must be even")
        elif len(self.card_values) * 2 > self.cards_number:
            raise ValueError(
                "The double number of card values must be less than or equal to number of cards"
            )

        self._create_cards()

    @property
    def cards_number(self) -> int:
        return self.rows_number * self.columns_number

    @property
    def cards(self) -> list[BattleCard]:
        return self._cards

    @property
    def matched_count(self) -> int:
        return self._matched_count

    @property
    def is_victory(self) -> bool:
        return self.mob.current_hp <= 0

    @property
    def is_defeated(self) -> bool:
        return self.player.current_hp <= 0

    @property
    def current_card(self) -> BattleCard | None:
        return self._current_card

    def set_current_card(self, position: int) -> None:
        self._current_card = self._cards[position]

    def clear_current_card(self) -> None:
        self._current_card = None

    def _create_cards(self) -> None:
        rest_number = self.cards_number // 2 % len(self.card_values)
        cycle_number = self.cards_number // 2 // len(self.card_values)

        for _ in range(cycle_number):
            for value in self.card_values:
                image, action = CARDS_MAP[value]
                self._cards.extend(
                    (
                        BattleCard(value, image, action),
                        BattleCard(value, image, action),
                    )
                )

        for value in sample(self.card_values, k=rest_number):
            image, action = CARDS_MAP[value]
            self._cards.extend(
                (
                    BattleCard(value, image, action),
                    BattleCard(value, image, action),
                )
            )

        shuffle(self._cards)

        for idx in range(len(self._cards)):
            self._cards[idx].position = idx

    def recreate_field(self) -> None:
        self._cards.clear()
        self._matched_count = 0
        self.clear_current_card()
        self._create_cards()
        self.pending_recreate = False

    def use_card_action(self):
        self.current_card.action(self.player, self.mob)

    def flip_card(self, position: int) -> None:
        flipped_card = self._cards[position]

        if flipped_card.state in self.clickable_states:
            flipped_card.state = "opened"

            if not self.current_card:
                self.set_current_card(position)
            elif self.current_card.value == flipped_card.value:
                self.current_card.state = "matched"
                flipped_card.state = "matched"
                self._matched_count += 2
                self.use_card_action()
                self.clear_current_card()
            else:
                self.pending_close = True
                self.player.take_damage(self.mob.damage)
                self.player.change_bonus_armor(-1)
                self.clear_current_card()

    def close_pending(self) -> None:
        if self.pending_close:
            for card in self.cards:
                if card.state == "opened":
                    card.state = "closed"
            self.pending_close = False

    def check_victory(self, victory_label: str, defeated_label: str) -> None:
        if self.is_victory:
            renpy.jump(victory_label)
        elif self.is_defeated:
            renpy.jump(defeated_label)
        elif self.matched_count == self.cards_number:
            self.pending_recreate = True
