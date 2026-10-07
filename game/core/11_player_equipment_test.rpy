# 11_player_equipment_test.rpy

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

        textbutton "Заполнить инвентарь":
            action [Function(inventory.add_item, short_sword), Function(inventory.add_item, shield)]

        textbutton "Очистить инвентарь":
            action Function(inventory.clear)


label test_player_equipment:
    scene bg gray_screen

    show screen player_equipment_test_screen
    pause
    return