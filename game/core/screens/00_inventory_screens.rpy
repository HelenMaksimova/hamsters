# 00_inventory_screens.rpy

screen inventory_screen():
    zorder 98
    modal True

    add Solid("#00000080")

    frame:
        at inventory_slide
        background "gui/inventory_frame.png"
        xalign 0.5
        yalign 1.0
        xsize 918
        ysize 418
        padding (20, 20)
        yoffset -130

        grid inventory.columns inventory.rows:
            spacing 5
            xalign 0.5
            yalign 0.0

            for idx in range(inventory.slots_number):
                button:
                    style "inventory_slot"
                    action Function(inventory.show_item_screen, idx)
                    sensitive inventory.is_slot_filled(idx)

                    if inventory.is_slot_filled(idx):
                        $ item = inventory.items[idx]
                        add item.icon:
                            xalign 0.5
                            yalign 0.5
                            xoffset -4
                            yoffset -4

                        if item.quantity > 1:
                            text "[item.quantity]":
                                color "#fff"
                                xalign 1.0
                                yalign 0.0
                                xoffset -24
                                yoffset 16
                                size 24


screen item_screen(item):
    zorder 99
    modal True

    add Solid("#00000080")

    frame:
        background "inventory/item_card.png"
        xalign 0.5
        yalign 0.5
        xsize 324
        ysize 524
        yoffset -200

        fixed:
            textbutton "X":
                xalign 1.0
                yalign 0.0
                xoffset -16
                action Hide()

            frame:
                background None
                padding (20, 20)
                xalign 0.5
                yalign 0.1

                vbox:
                    xalign 0.5
                    spacing 10

                    text item.title:
                        xalign 0.5

                    add item.image:
                        xalign 0.5

                    if item.type == "potion":
                        textbutton "Использовать":
                            xalign 0.5
                            action [Hide(), Function(inventory.use_item, item)]

                    elif item.is_active:
                        textbutton "Снять":
                            xalign 0.5
                            action [Hide(), Function(player_equipment.take_off, item)]
                            sensitive not inventory.is_full

                    elif not item.is_active:
                        textbutton "Экипировать":
                            xalign 0.5
                            action [Hide(), Function(player_equipment.take_on, item)]


screen player_equipment_screen():
    modal True

    frame:
        background "inventory/player_equipment_card.png"
        xalign 0.5
        yalign 0.5
        xsize 524
        ysize 774
        yoffset -100

        button:
            style "inventory_slot"
            xalign 0.5
            yalign 0.1
            sensitive not player_equipment.head.is_empty
            if not player_equipment.head.is_empty:
                add player_equipment.head.item.icon:
                    xalign 0.5
                    yalign 0.5
                action Show("item_screen", item=player_equipment.head.item)

        hbox:
            xalign 0.5
            yalign 0.35
            spacing 40

            button:
                style "inventory_slot"
                sensitive not player_equipment.hands[0].is_empty
                if not player_equipment.hands[0].is_empty:
                    add player_equipment.hands[0].item.icon:
                        xalign 0.5
                        yalign 0.5
                    action Show("item_screen", item=player_equipment.hands[0].item)

            button:
                style "inventory_slot"
                sensitive not player_equipment.body.is_empty
                if not player_equipment.body.is_empty:
                    add player_equipment.body.item.icon:
                        xalign 0.5
                        yalign 0.5
                    action Show("item_screen", item=player_equipment.body.item)

            button:
                style "inventory_slot"
                sensitive not player_equipment.hands[1].is_empty
                if not player_equipment.hands[1].is_empty:
                    add player_equipment.hands[1].item.icon:
                        xalign 0.5
                        yalign 0.5
                    action Show("item_screen", item=player_equipment.hands[1].item)

        hbox:
            xalign 0.5
            yalign 0.65
            spacing 10

            for idx in range(player_equipment.accessories_slots_number):
                button:
                    style "inventory_slot"
                    sensitive not player_equipment.accessories[idx].is_empty
                    if not player_equipment.accessories[idx].is_empty:
                        add player_equipment.accessories[idx].item.icon:
                            xalign 0.5
                            yalign 0.5
                        action Show("item_screen", item=player_equipment.accessories[idx].item)

        hbox:
            xalign 0.5
            yalign 0.9
            spacing 10

            frame:
                background "inventory/pe_armor_icon.png"
                xalign 0.5
                xsize 104
                ysize 104
                text "[player.armor]":
                    style "battle_parameter_text"
                    size 30

            frame:
                background "inventory/pe_health_icon.png"
                xalign 0.5
                xsize 104
                ysize 104
                text "[player.current_hp]/[player.max_hp]":
                    style "battle_parameter_text"
                    size 25

            frame:
                background "inventory/pe_heal_icon.png"
                xalign 0.5
                xsize 104
                ysize 104
                text "[player.heal]":
                    style "battle_parameter_text"
                    size 30

            frame:
                background "inventory/pe_damage_icon.png"
                xalign 0.5
                xsize 104
                ysize 104
                text "[player.damage]":
                    style "battle_parameter_text"
                    size 30
