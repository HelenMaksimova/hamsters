# 02_artem_room.rpy

label artem_room:
    scene bg artem_room
    artem smile 'Наконец-то я дома!'
    artem joyful 'Ненавижу школу! Здорово, что сегодня пятница и можно хоть на пару дней забыть про всю эту скучищу'
    mother_voice 'Милый, не забудь, что вам задали к понедельнику доклад по биологии!'
    artem -joyful 'Вот блин...'
    mother_voice 'А завтра мы едем к бабушке с дедушкой на дачу. Они просили помочь им с огородом'
    artem sad 'Вот блин!'
    mother_voice 'И к воскресенью тебе нужно закончить разучивать пьесу'
    mother_voice 'Виталий Иванович говорит, что ты отлыниваешь, так что придётся мне проследить за процессом!'
    artem upset 'Вот блин!!!'
    mother_voice 'Тём, ты меня слышал?'
    artem -upset 'Да, мам! Я понял. Можно хотя бы сегодня отдохнуть?'
    mother_voice 'Дело, конечно, твоё, солнышко, но я бы на твоём месте постаралась сделать уроки на понедельник сегодня. Ну или доклад'
    artem sad 'Да, мам... Ну вот и отдохнул пару дней, называется'
    artem -sad 'Ладно, чем бы и вправду заняться?'
    jump artem_room_exploring

label artem_room_exploring:
    scene bg artem_room
    show screen artem_room_exploring_screen
    pause
    return

label artem_room_hamster_photo():
    show screen image_window_screen('hamster_photo')
    artem sad 'Уже два года прошло, а мне всё ещё грустно...'
    hide screen image_window
    jump artem_room_exploring

label artem_room_go_sleep():
    menu:
        'Идти спать':
            artem 'Пожалуй, пора баиньки'
            jump test_battle_exploring
        'Пока рано ложиться':
            jump artem_room_exploring


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
