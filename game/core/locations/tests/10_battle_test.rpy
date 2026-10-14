# 10_battle_test.rpy

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
