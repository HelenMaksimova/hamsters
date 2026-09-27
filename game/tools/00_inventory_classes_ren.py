"""renpy
init -997 python:
"""
from dataclasses import dataclass, field


@dataclass
class Item:
    title: str
    icon: str
    image: str
    quantity: int = 1
    description: str | None = None

    def use(self) -> None:
        pass


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
        index = next((idx for idx, element in enumerate(self._items) if element.title == item.title), None)

        if index is not None:
            self._items[index].quantity += 1
        elif len(self._items) + 1 <= self.slots_number:
            self._items.append(item)

    def remove_item(self, position: int) -> None:
        try:
            self._items.pop(position)
        except IndexError:
            raise ValueError("Inventory items is empty or item position is out of range")

    def is_slot_filled(self, position) -> bool:
        return position < len(self._items)

    def use_item(self, position) -> None:
        try:
            item = self._items[position]
        except IndexError:
            raise ValueError("Inventory items is empty or item position is out of range")

        item.quantity -= 1

        item.use()

        if item.quantity <= 0:
            self.remove_item(position)

    def show_item_screen(self, position: int) -> None:
        if self.is_slot_filled(position):
            renpy.show_screen("item_screen", inventory=self, position=position)

    def toggle_inventory(self):
        if renpy.get_screen("inventory_screen"):
            renpy.hide_screen("inventory_screen")
        else:
            renpy.show_screen("inventory_screen", inventory=self)