# 00_styles.rpy

style paw_button:
    background "gui/[prefix_]paw_button.png"
    xsize 92
    ysize 80


style battle_button:
    background "gui/[prefix_]battle_button.png"
    xsize 124
    ysize 124


style inventory_slot:
    background "gui/[prefix_]inventory_slot.png"
    xsize 124
    ysize 124


style battle_parameter_text:
    xalign 0.5
    yalign 0.5
    xoffset -3
    font "fonts/custom_font_1.otf"
    size 50

transform inventory_slide:
    on show:
        yoffset 500
        easein 0.3 yoffset 0
    on hide:
        easeout 0.3 yoffset 500