# 10_test_buttle.rpy

init python:
    def check_victory(mob: "Mob", buttle: "ButtleData"):
        if mob.current_health <= 0:
            buttle.defeat(mob)
            renpy.jump("victory")


screen buttle_choice_screen():
    modal True

    vbox:
        textbutton "[dog.name]":
            action [Hide(), Jump("battle_dog")]
            sensitive test_buttle.is_active(dog)
        textbutton "[cat.name]":
            action [Hide(), Jump("battle_cat")]
            sensitive test_buttle.is_active(cat)


screen battle_screen(mob):
    vbox:
        text "Противник: [mob.name]"
        text "Здоровье: [mob.current_health]/[mob.max_health]"
        textbutton "Атаковать":
            action [
                Function(mob.take_damage),
                Function(check_victory, mob, test_buttle)
            ]


label artem_dream_exploring:
    show screen buttle_choice_screen
    pause
    return


label battle_dog:
    show screen battle_screen(dog)
    pause
    return


label battle_cat:
    show screen battle_screen(cat)
    pause
    return


label victory:
    hide screen battle_screen
    "Вы победили!"
    jump artem_dream_exploring
