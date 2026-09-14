# 10_test_battle.rpy

screen battle_choice_screen():
    modal True

    vbox:
        button:
            style "battle_button"
            action [Hide(), Jump("test_battle")]


screen battle_screen():
    modal True

    vbox:
        textbutton "Выйти":
            action [
                Hide(), Jump("test_battle_exploring")
            ]

    grid 4 4:
        spacing 10
        xalign 0.5
        yalign 0.5

        for i in range(16):
            button:
                style "battle_button"
                action NullAction()


label test_battle_exploring:
    scene bg gray_screen
    show screen battle_choice_screen
    pause
    return


label test_battle:
    show screen battle_screen
    pause
    return
