# 00_screens.rpy

screen image_window(img):
    vbox:
        add img
        xalign 0.5
        yalign 0.1


transform inventory_slide:
    on show:
        yoffset 500
        easein 0.3 yoffset 0
    on hide:
        easeout 0.3 yoffset 500


screen inventory:
    zorder 99
    modal True

    add Solid("#00000040")

    frame:
        at inventory_slide
        background "gui/inventory_frame.png"
        xalign 0.5
        yalign 1.0
        xsize 918
        ysize 418
        padding (20, 20)
        yoffset -130

        grid 5 2:
            spacing 15
            xalign 0.5
            yalign 0.5

            for i in range(10):
                button:
                    style "inventory_slot"
                    xysize (150, 150)
                    action NullAction()
