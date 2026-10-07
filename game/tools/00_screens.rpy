# 00_screens.rpy

transform inventory_slide:
    on show:
        yoffset 500
        easein 0.3 yoffset 0
    on hide:
        easeout 0.3 yoffset 500


screen test_screen():
    modal True

    vbox:
        spacing 15
        xalign 0.5
        yalign 0.5

        textbutton "Комната Артёма":
            action [Hide(), Jump("artem_room")]

        textbutton "Боёвка":
            action [Hide(), Jump("test_battle")]

        textbutton "Экипировка":
            action [Hide(), Jump("test_player_equipment")]

screen image_window_screen(img):
    vbox:
        add img
        xalign 0.5
        yalign 0.1


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
                            action [Hide(), Function(inventory.use_item, position)]

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
        ysize 624
        yoffset -200

        button:
            style "inventory_slot"
            xalign 0.5
            yalign 0.05
            sensitive not player_equipment.head.is_empty
            if not player_equipment.head.is_empty:
                add player_equipment.head.item.icon:
                    xalign 0.5
                    yalign 0.5
                action Show("item_screen", item=player_equipment.head.item)

        hbox:
            xalign 0.5
            yalign 0.3
            spacing 60

            frame:
                background "inventory/pe_armor_icon.png"
                xalign 0.5
                xsize 124
                ysize 124
                text "[player.armor]":
                    style "battle_parameter_text"
                    size 40

            frame:
                background "inventory/pe_health_icon.png"
                xalign 0.5
                xsize 124
                ysize 124
                text "[player.current_hp]/[player.max_hp]":
                    style "battle_parameter_text"
                    size 40

            frame:
                background "inventory/pe_damage_icon.png"
                xalign 0.5
                xsize 124
                ysize 124
                text "[player.damage]":
                    style "battle_parameter_text"
                    size 40

        hbox:
            xalign 0.5
            yalign 0.55
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
            yalign 0.9
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

