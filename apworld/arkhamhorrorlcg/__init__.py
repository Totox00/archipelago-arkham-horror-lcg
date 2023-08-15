# world/arkhamhorrorlcg/__init__.py
from typing import Dict, Set, List

from BaseClasses import MultiWorld, Region, Item, Entrance, Tutorial, ItemClassification
from Options import Toggle

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, add_rule, add_item_rule

from .Items import ArkhamHorrorLCGItem, AHLCGItemCategory, item_dictionary, key_item_names, items
from .Locations import ArkhamHorrorLCGLocation, AHLCGLocationCategory, location_tables, location_dictionary
from .Options import arkham_horror_lcg_options


class ArkhamHorrorLCGWeb(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up the Archipelago Arkham Horror LCG randomizer on Tabletop Simulator.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Toto"]
    )

    tutorials = [setup_en]


class ArkhamHorrorLCGWorld(World):
    """
    Arkham Horror: The Card Game can be played either irl or through tabletop simulator.
    This world requires a custom scenario made specifically for Archipelago, and it is
    advised to play using Tabletop Simulator.
    """

    game = "Arkham Horror LCG"
    option_definitions = arkham_horror_lcg_options
    topology_present = True
    web = ArkhamHorrorLCGWeb()
    data_version = 0
    base_id = 20000000
    required_client_version = (0, 1, 0)
    item_name_to_id = ArkhamHorrorLCGItem.get_name_to_id()
    location_name_to_id = ArkhamHorrorLCGLocation.get_name_to_id()

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.locked_items = []
        self.locked_locations = []
        self.main_path_locations = []

    # def generate_early(self):

    def create_regions(self):
        progressive_location_table = []

        # Create Vanilla Regions
        regions: Dict[str, Region] = {}
        regions["Menu"] = self.create_region("Menu", progressive_location_table)
        regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in [
            "Arkham",
            "Dunwich",
        ]})

        # Connect Regions
        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"Go To {to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])

        regions["Menu"].exits.append(Entrance(self.player, "Start", regions["Menu"]))
        self.multiworld.get_entrance("Start", self.player).connect(regions["Arkham"])

        create_connection("Arkham", "Dunwich")

    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)

        for location in location_table:
            new_location = ArkhamHorrorLCGLocation(
                self.player,
                location.name,
                location.category,
                self.location_name_to_id[location.name],
                new_region
            )

            if region_name == "Menu":
                add_item_rule(new_location, lambda item: not item.advancement)

            new_region.locations.append(new_location)

        self.multiworld.regions.append(new_region)
        return new_region

    def create_items(self):
        num_required_extra_items = 0

        itempool: List[ArkhamHorrorLCGItem] = []
        itempool += [self.create_item(name) for name in items]

        # Extra filler items for locations containing SKIP items
        itempool += [self.create_filler() for _ in range(num_required_extra_items)]

        # Add items to itempool
        self.multiworld.itempool += itempool

    def create_item(self, name: str) -> Item:
        data = self.item_name_to_id[name]

        if item_dictionary[name].category == AHLCGItemCategory.KEY:
            item_classification = ItemClassification.progression
        elif item_dictionary[name].category == AHLCGItemCategory.TRAP:
            item_classification = ItemClassification.trap
        else:
            item_classification = ItemClassification.useful

        return ArkhamHorrorLCGItem(name, item_classification, data, self.player)

    def get_filler_item_name(self) -> str:
        return "1 XP"

    def set_rules(self) -> None:
        # Define the access rules to the entrances
        set_rule(self.multiworld.get_entrance("Go To Dunwich", self.player),
                 lambda state: state.has("Train Ticket", self.player))

        # Define the access rules to some specific locations
        set_rule(self.multiworld.get_location("Some location", self.player),
                 lambda state: state.has("Some item", self.player))

        self.multiworld.completion_condition[self.player] = lambda state: \
            state.has("Some victory condition", self.player)

    def fill_slot_data(self) -> Dict[str, object]:

        return {}
