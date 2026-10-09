# 00_test_screens.rpy

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


screen player_equipment_test_screen():
    modal True

    vbox:
        xalign 1.0
        yalign 0.0

        textbutton "X":
            action [Hide(), Jump("test")]

    vbox:
        spacing 15
        xalign 0.5
        yalign 0.5

        textbutton "Добавить щит и меч":
            action [Function(inventory.add_item, short_sword), Function(inventory.add_item, shield)]

        textbutton "Добавить зелье":
            action Function(add_potion)

        textbutton "Очистить инвентарь":
            action Function(inventory.clear)
