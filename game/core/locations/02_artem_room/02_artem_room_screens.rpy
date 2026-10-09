# 02_artem_room_screens.rpy

screen artem_room_exploring_screen():
    modal True

    button:
        style "paw_button"
        xalign 0.1
        yalign 0.1
        action [Hide(), Jump("artem_room_hamster_photo")]

    button:
        style "paw_button"
        xalign 0.1
        yalign 0.7
        action [Hide(), Jump("artem_room_go_sleep")]
