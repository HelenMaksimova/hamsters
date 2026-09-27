# 10_test_battle.rpy

init python:
    def add_item(num: int):
        items_map = {
            1: ("Предмет_01", "inventory/item_01_icon.png", "inventory/item_01.png"),
            2: ("Предмет_02", "inventory/item_02_icon.png", "inventory/item_02.png"),
            3: ("Предмет_03", "inventory/item_03_icon.png", "inventory/item_03.png"),
            4: ("Предмет_04", "inventory/item_04_icon.png", "inventory/item_04.png"),
        }
        params = items_map[num]
        inventory.add_item(Item(*params))


screen battle_screen(battle):
    modal True

    vbox:
        xalign 1.0
        yalign 0.0

        textbutton "X":
            action [Hide(), Jump("test")]

    vbox:
        yoffset 10
        xalign 0.5
        yalign 0.0

        text "[battle.mob.name]":
            font "fonts/custom_font_1.otf"
            size 60

    hbox:
        xalign 0.5
        yoffset 80
        xfill True

        vbox:
            spacing 15
            xalign 0.5
            yalign 0.0

            frame:
                background "battle/portrait_frame.png"
                xalign 0.5
                xsize 274
                ysize 274
                add battle.mob.battle_icon:
                    xalign 0.5
                    yalign 1.0
                    xoffset -10
                    yoffset -10

            hbox:
                xalign 0.5
                spacing 10

                frame:
                    background "battle/health_icon.png"
                    xalign 0.5
                    xsize 150
                    ysize 150
                    text "[battle.mob.current_hp]":
                        style "battle_parameter_text"

                frame:
                    background "battle/damage_icon.png"
                    xalign 0.5
                    xsize 150
                    ysize 150
                    text "[battle.mob.damage]":
                        style "battle_parameter_text"


        grid battle.columns_number battle.rows_number:
            spacing 5
            xalign 0.5
            yalign 0.5

            for i in range(battle.cards_number):
                button:
                    style "battle_button"
                    action [Function(battle.flip_card, i), Function(battle.check_victory, "victory", "defeated")]

                    if battle.cards[i].state in {"opened", "matched"}:
                        background battle.cards[i].image
                    else:
                        background "gui/[prefix_]battle_button.png"

        vbox:
            spacing 15
            xalign 0.5
            yalign 0.0

            frame:
                background "battle/portrait_frame.png"
                xalign 0.5
                xsize 274
                ysize 274
                add battle.player.battle_icon:
                    xalign 0.5
                    yalign 1.0
                    xoffset -10
                    yoffset -10

            hbox:
                xalign 0.5
                spacing 10

                frame:
                    background "battle/health_icon.png"
                    xalign 0.5
                    xsize 150
                    ysize 150
                    text "[battle.player.current_hp]":
                        style "battle_parameter_text"

                frame:
                    background "battle/armor_icon.png"
                    xalign 0.5
                    xsize 150
                    ysize 150
                    text "[battle.player.armor]":
                        style "battle_parameter_text"

            frame:
                background "battle/damage_icon.png"
                xalign 0.5
                xsize 150
                ysize 150
                text "[battle.player.damage]":
                    style "battle_parameter_text"

    if battle.pending_close:
            timer 1.0 action Function(battle.close_pending)

    if battle.pending_recreate:
            timer 1.0 action Function(battle.recreate_field)


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

    $ battle = BattleGround(
        (0, 1, 2),
        mob=mob,
        player=player,
        rows_number=4,
        columns_number=4
    )
    show screen battle_screen(battle)
    pause
    return
