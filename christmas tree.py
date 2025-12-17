import time
import random

# ======================
# Screen config
# ======================
width = 60
height = 26

# ======================
# Visual elements
# ======================
flakes = ['*', '.', '❄', '•']

sky_colors = [
    "\033[38;5;111m",  # icy blue
    "\033[38;5;153m",  # frosty lavender
    "\033[38;5;195m",  # pale moonlight
]

# Christmas light colors (ANSI)
light_colors = [
    "\033[38;5;196m",  # vivid red
    "\033[38;5;226m",  # yellow
    "\033[38;5;46m",   # green
]

reset = "\033[0m"

# ======================
# Christmas tree (fixed)
# ======================
tree = [
    "          *",
    "         ***",
    "        *****",
    "       *******",
    "      *********",
    "     ***********",
    "    *************",
    "         |||",
    "         |||"
]

TREE_BASE_Y = height - len(tree) - 2

# ======================
# State variables
# ======================
snow = []
ground = [1 for _ in range(width)]
star_pulse = 0

# ======================
# Terminal helpers
# ======================
def hide_cursor():
    print("\033[?25l", end="")

def show_cursor():
    print("\033[?25h", end="")

def cursor_to_top():
    print("\033[H", end="")

def clear_screen():
    print("\033[2J", end="")

# ======================
# Snow logic
# ======================
def create_flake():
    return {
        "x": random.randint(0, width - 1),
        "y": 0,
        "char": random.choice(flakes),
        "speed": random.choice([1, 1, 2]),
        "wind": random.choice([-1, 0, 1]),
        "color": random.choice(sky_colors)
    }

def maybe_add_flake():
    if random.random() < 0.5:
        snow.append(create_flake())

def update_snow():
    for f in list(snow):
        f["y"] += f["speed"]
        f["x"] = (f["x"] + f["wind"]) % width

        if f["y"] >= height - ground[f["x"]]:
            snow.remove(f)
            ground[f["x"]] = min(ground[f["x"]] + 1, height - 1)

def draw_snow(buffer):
    for f in snow:
        if 0 <= f["y"] < height and 0 <= f["x"] < width:
            buffer[f["y"]][f["x"]] = f["color"] + f["char"] + reset

# ======================
# Tree drawing (FIXED)
# ======================
def draw_tree(buffer):
    global star_pulse

    start_y = TREE_BASE_Y
    start_x = (width // 2) - (len(tree[-1]) // 2)

    for i, line in enumerate(tree):
        for j, char in enumerate(line):
            y = start_y + i
            x = start_x + j

            if not (0 <= y < height and 0 <= x < width):
                continue

            # Top star glow
            if i == 0 and char == "*":
                glow = light_colors[star_pulse % len(light_colors)]
                buffer[y][x] = glow + "★" + reset

            # Tree lights
            elif char == "*" and random.random() < 0.15:
                buffer[y][x] = random.choice(light_colors) + "*" + reset

            else:
                buffer[y][x] = char

# ======================
# Main loop
# ======================
print("❄ Press Ctrl+C to stop ❄\n")
time.sleep(1)

hide_cursor()
clear_screen()

try:
    while True:
        buffer = [[" " for _ in range(width)] for _ in range(height)]

        draw_tree(buffer)
        draw_snow(buffer)

        cursor_to_top()
        print("\n".join("".join(row) for row in buffer))

        maybe_add_flake()
        update_snow()

        star_pulse += 1
        time.sleep(0.1)

except KeyboardInterrupt:
    show_cursor()
    print("\n❄ Scene closed ❄")
