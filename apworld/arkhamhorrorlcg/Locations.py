from enum import IntEnum
from typing import Optional, NamedTuple, Dict

from BaseClasses import Location, Region


class AHLCGLocationCategory(IntEnum):
    EMPTY_LOCATION = 0
    KILLED_ENEMY = 1


class AHLCGLocationData(NamedTuple):
    name: str
    category: AHLCGLocationCategory


class ArkhamHorrorLCGLocation(Location):
    game: str = "Arkham Horror LCG"
    category: AHLCGLocationCategory

    def __init__(
            self,
            player: int,
            name: str,
            category: AHLCGLocationCategory,
            address: Optional[int] = None,
            parent: Optional[Region] = None):
        super().__init__(player, name, address, parent)
        self.category = category

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 20000000
        table_offset = 100

        table_order = [
            "Arkham",
            "Dunwich"
        ]

        output = {}
        for i, table in enumerate(table_order):
            output.update({location_data.name: id for id, location_data in enumerate(
                location_tables[table], base_id + (table_offset * i))})

        return output


location_tables = {
    "Arkham": [
        AHLCGLocationData("Arkham: SomeLocation",               AHLCGLocationCategory.EMPTY_LOCATION),
    ],
    "Dunwich": [
        AHLCGLocationData("Dunwich: SomeEnemy",                AHLCGLocationCategory.KILLED_ENEMY),
    ]
}

location_dictionary: Dict[str, AHLCGLocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})
