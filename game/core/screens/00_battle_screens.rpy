# 00_battle_screens.rpy

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

            hbox:
                xalign 0.5
                spacing 10

                frame:
                    background "battle/heal_icon.png"
                    xalign 0.5
                    xsize 150
                    ysize 150
                    text "[battle.player.heal]":
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