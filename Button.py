button_count = 9
button_size = 80
button_y = 30
button_names = [
    "Create",
    "Create Bulk",
    "Grabbing",
    "Delete",
    "Delete Bulk",
    "Delete All",
    "Debug \nmode",
    "Change \nColor",
    "Change \nBulk Color"
]
button_states = [True, False, False, False, False, False, False, False, False]


def button_draw(w):
    button_spacing = (w - button_size * button_count) / (button_count + 1)
    for i in range(button_count):
        button_x = button_spacing * (i + 1) + button_size * i
        fill(255)
        stroke(0)
        strokeWeight(5)
        if button_states[i]:
            fill(100)  # Green color for pressed buttons
        rect(button_x, button_y, button_size, button_size)
        textSize(14)
        textAlign(CENTER, CENTER)
        fill(0)
        text(button_names[i], button_x + button_size / 2, button_y + button_size / 2)
