# 01_init_data.rpy

##################################### CHARACTERS #####################################

define artem = Character('Артём', color="#1e82b1", image='artem')
define mother_voice = Character('Голос мамы', color="#d39e61", image='default_char')

default inventory = Inventory()
default player = Player(10, "battle/player_battle_icon.png")
default player_equipment = PlayerEquipment()
default context = Context()

default short_sword = EquipmentItem(
        "Короткий меч",
        "inventory/sword_item_icon.png",
        "inventory/sword_item.png",
        "hand",
        take_on_action="player_weapon_take_on_action",
        take_off_action="player_weapon_take_off_action",
    )

default shield = EquipmentItem(
        "Щит",
        "inventory/shield_item_icon.png",
        "inventory/shield_item.png",
        "hand",
        take_on_action="player_armor_take_on_action",
        take_off_action="player_armor_take_off_action",
    )
