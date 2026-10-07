"""renpy
init -997 python:
"""

from dataclasses import dataclass, field
from itertools import chain
from typing import Literal


def player_armor_take_on_action():
    player.change_base_armor(1)


def player_armor_take_off_action():
    player.change_base_armor(-1)


def player_weapon_take_on_action():
    player.change_base_damage(1)


def player_weapon_take_off_action():
    player.change_base_damage(-1)


def player_heal_potion_action():
    player.change_bonus_heal(3)


ACTIONS = {
    "player_armor_take_on_action": player_armor_take_on_action,
    "player_armor_take_off_action": player_armor_take_off_action,
    "player_weapon_take_on_action": player_weapon_take_on_action,
    "player_weapon_take_off_action": player_weapon_take_off_action,
    "player_heal_potion_action": player_heal_potion_action,
}


@dataclass
class BaseItem:
    title: str
    icon: str
    image: str
    type: Literal["body", "hand", "head", "accessory", "potion"]
    description: str | None = None
    action: str | None = None

    @property
    def is_equipment(self) -> bool:
        return self.type in ["body", "hand", "head", "accessory"]


@dataclass
class Item(BaseItem):
    quantity: int = 1

    def use(self) -> None:
        self.quantity -= 1

        self.quantity = max(self.quantity, 0)

        if self.action:
            ACTIONS[self.action]()


@dataclass
class EquipmentItem(BaseItem):
    is_active: bool = False
    take_on_action: str | None = None
    take_off_action: str | None = None

    def use(self) -> None:
        if self.action:
            ACTIONS[self.action]()

    def take_on(self):
        self.is_active = True

        if self.take_on_action:
            ACTIONS[self.take_on_action]()

    def take_off(self):
        self.is_active = False

        if self.take_off_action:
            ACTIONS[self.take_off_action]()

    @property
    def quantity(self) -> int:
        return 1


@dataclass
class Inventory:
    _items: list[Item] = field(default_factory=list, init=False)
    _slots_number: int = field(default=6, init=False)
    _row_size: int = field(default=6, init=False)

    def __post_init__(self) -> None:
        if self._slots_number < 1 or self._row_size < 1:
            raise ValueError("slots_number and row_size must be greater than 1")
        if self._slots_number % self._row_size:
            raise ValueError("slots_number must be a multiple of row_size")

    @property
    def rows(self) -> int:
        return self._slots_number // self._row_size

    @property
    def columns(self) -> int:
        return self._row_size

    @property
    def slots_number(self) -> int:
        return self._slots_number

    @property
    def items(self) -> list[Item]:
        return self._items

    @property
    def is_full(self) -> bool:
        return len(self._items) >= self._slots_number

    def items_by_type(self, type_: str) -> list[Item]:
        return [item for item in self._items if item.type == type_]

    def increase_slots(self, number: int) -> None:
        if (self._slots_number + number) % self._row_size:
            raise ValueError("slots_number must be a multiple of row_size")

        self._slots_number += number

    def decrease_slots(self, number: int) -> None:
        if self._slots_number - number < 1:
            raise ValueError("slots_number must be greater than 1")
        if (self._slots_number - number) % self._row_size:
            raise ValueError("slots_number must be a multiple of row_size")

        self._slots_number -= number

    def set_row_size(self, number: int) -> None:
        if number < 1:
            raise ValueError("row_size must be greater than 1")
        if self._slots_number % number:
            raise ValueError("slots_number must be a multiple of row_size")

        self._row_size = number

    def add_item(self, item: Item) -> None:
        if self.is_full:
            return

        index = next(
            (
                idx
                for idx, element in enumerate(self._items)
                if element.title == item.title
            ),
            None,
        )
        if item.is_equipment:
            self._items.append(item)
        elif index is not None:
            self._items[index].quantity += 1
        elif len(self._items) + 1 <= self.slots_number:
            self._items.append(item)

    def remove_item(
        self, position: int | None = None, item: Item | None = None
    ) -> None:
        if position is None and item is None:
            raise ValueError(
                "One of parameters: position or item must be defined"
            )

        if position is not None:
            try:
                self._items.pop(position)
            except IndexError:
                raise ValueError(
                    "Inventory items is empty or item position is out of range"
                )
        elif item is not None:
            try:
                self._items.remove(item)
            except ValueError:
                raise ValueError("Inventory has not this item")

    def clear(self) -> None:
        self._items.clear()

    def is_slot_filled(self, position: int) -> bool:
        return position < len(self._items)

    def use_item(self, position: int) -> None:
        try:
            item = self._items[position]
        except IndexError:
            raise ValueError(
                "Inventory items is empty or item position is out of range"
            )

        item.use()

        if item.quantity <= 0:
            self.remove_item(item=item)

    def show_item_screen(self, position: int) -> None:
        if self.is_slot_filled(position):
            renpy.show_screen("item_screen", item=self.items[position])

    def toggle_screen(self) -> None:
        if renpy.get_screen("inventory_screen"):
            renpy.hide_screen("inventory_screen")
        else:
            renpy.show_screen("inventory_screen")


@dataclass
class PlayerEquipmentSlot:
    item: EquipmentItem | None = None

    @property
    def is_empty(self) -> bool:
        return not bool(self.item)

    def take_on(self, item: EquipmentItem) -> None:
        self.item = item
        inventory.remove_item(item=item)
        self.item.take_on()

    def take_off(self) -> None:
        inventory.add_item(self.item)
        self.item.take_off()
        self.item = None


@dataclass
class PlayerEquipment:
    accessories_slots_number: int = 2
    _body: PlayerEquipmentSlot | None = field(default=None, init=False)
    _head: PlayerEquipmentSlot | None = field(default=None, init=False)
    _hands: list[PlayerEquipmentSlot] = field(default_factory=list, init=False)
    _accessories: list[PlayerEquipmentSlot] = field(
        default_factory=list, init=False
    )

    def __post_init__(self) -> None:
        self._create_slots()

    @property
    def attrs_map(self) -> dict[str, str]:
        return {
            "body": "_body",
            "head": "_head",
            "hand": "_hands",
            "accessory": "_accessories",
        }

    @property
    def body(self) -> PlayerEquipmentSlot:
        return self._body

    @property
    def head(self) -> PlayerEquipmentSlot:
        return self._head

    @property
    def hands(self) -> list[PlayerEquipmentSlot]:
        return self._hands

    @property
    def accessories(self) -> list[PlayerEquipmentSlot]:
        return self._accessories

    @property
    def equipment(self) -> list[EquipmentItem]:
        return [
            slot.item
            for slot in chain(
                self._accessories, self._hands, (self._body,), (self._head,)
            )
            if slot.item
        ]

    @property
    def slots(self) -> list[PlayerEquipmentSlot]:
        return [
            slot
            for slot in chain(
                self._accessories, self._hands, (self._body,), (self._head,)
            )
            if slot.item
        ]

    @staticmethod
    def _get_empty_slot(*slots: PlayerEquipmentSlot) -> PlayerEquipmentSlot:
        for slot in slots:
            if slot.is_empty:
                return slot
        slots[0].take_off()
        return slots[0]

    def _create_slots(self) -> None:
        self._body = PlayerEquipmentSlot()
        self._head = PlayerEquipmentSlot()
        self._hands = [PlayerEquipmentSlot() for _ in range(2)]
        self._accessories = [
            PlayerEquipmentSlot() for _ in range(self.accessories_slots_number)
        ]

    def take_on(self, item: EquipmentItem) -> None:
        value = getattr(self, self.attrs_map.get(item.type))
        slots = value if isinstance(value, list) else [value]
        slot = self._get_empty_slot(*slots)
        slot.take_on(item)

    def take_off(self, item: EquipmentItem) -> None:
        for slot in self.slots:
            if slot.item == item:
                slot.take_off()

    def toggle_screen(self) -> None:
        if renpy.get_screen("player_equipment_screen"):
            renpy.hide_screen("player_equipment_screen")
        else:
            renpy.show_screen("player_equipment_screen")
