# 10_test_battle.rpy

screen battle_choice_screen():
    modal True

    vbox:
        button:
            style "battle_button"
            action [Hide(), Jump("test_battle")]


screen battle_screen(battle):
    modal True

    vbox:
        textbutton "Выйти":
            action [
                Hide(), Jump("test_battle_exploring")
            ]

    grid battle.columns_number battle.rows_number:
        spacing 10
        xalign 0.5
        yalign 0.5

        for i in range(battle.cards_number):
            button:
                style "battle_button"
                action [Function(battle.flip_card, i), Function(battle.check_victory, "victory")]

                if battle.cards[i].state in {"opened", "matched"}:
                    background battle.cards[i].image
                else:
                    background "gui/[prefix_]battle_button.png"

    if battle.pending_close:
            timer 1.0 action Function(battle.close_pending)


label victory:
    hide screen battle_screen
    "Вы победили!"
    jump test_battle_exploring


label test_battle_exploring:
    scene bg gray_screen
    show screen battle_choice_screen
    pause
    return


label test_battle:
    $ battle = BattleGround(
        (0, 1, 2, 3),
        (
            "test_battle/battle_value_0.png",
            "test_battle/battle_value_1.png",
            "test_battle/battle_value_2.png",
            "test_battle/battle_value_3.png",
        ),
        rows_number=4,
        columns_number=4
    )
    show screen battle_screen(battle)
    pause
    return
