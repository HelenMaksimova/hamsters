# 10_battle_test.rpy

label victory:
    hide screen battle_screen
    "Вы победили!"
    jump test

label defeated:
    hide screen battle_screen
    "Вы проиграли!"
    jump test

label test_battle:
    scene bg battle_forest_screen

    $ mob = Mob("Лесной Котёнок", 4, "battle/forest_kitten.png")
    $ context.battle.mob = mob
    $ context.game_state.in_battle = True

    $ battle = BattleGround(
        (0, 1, 2),
        rows_number=4,
        columns_number=4
    )
    show screen battle_screen(battle)
    pause
    return
