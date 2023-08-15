from enum import IntEnum
from typing import NamedTuple

from BaseClasses import Item


class AHLCGItemCategory(IntEnum):
    KEY = 0
    ASSET = 1
    XP = 2
    META = 3
    TRAP = 4


class AHLCGItemData(NamedTuple):
    name: str
    max_copies: int
    category: AHLCGItemCategory


class ArkhamHorrorLCGItem(Item):
    game: str = "Arkham Horror LCG"

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 20000000
        return {item_data.name: id for id, item_data in enumerate(items, base_id)}


key_item_names = {
    "Boat Ticket",
    "Train Ticket"
}


items = [AHLCGItemData(row[0], row[1], row[2]) for row in [
    # Key
    ("Boat Ticket",  2, AHLCGItemCategory.KEY),
    ("Train Ticket", 1, AHLCGItemCategory.KEY),

    # Story assets
    ("Some Ally", 1, AHLCGItemCategory.ASSET),
    ("meta_Multiworld", 1, AHLCGItemCategory.META),

    # XP
    ("1 XP", -1, AHLCGItemCategory.XP),

    # Trap
    ("Something bad", -1, AHLCGItemCategory.TRAP)
]]

item_dictionary = {item_data.name: item_data for item_data in items}
