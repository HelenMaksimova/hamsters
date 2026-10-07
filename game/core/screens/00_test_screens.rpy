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
