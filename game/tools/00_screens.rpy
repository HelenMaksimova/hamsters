# 00_screens.rpy

screen image_window(img):
    vbox:
        add img
        xalign 0.5
        yalign 0.1


transform inventory_slide:
    on show:
        yoffset 500
        easein 0.3 yoffset 0
    on hide:
        easeout 0.3 yoffset 500


screen inventory_screen (inventory):
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


screen item_screen(inventory, position):
    zorder 99
    modal True

    $ item = inventory.items[position]

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

                    textbutton "Использовать":
                        xalign 0.5
                        action [Hide(), Function(inventory.use_item, position)]