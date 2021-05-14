from asciimatics.screen import Screen

# | key       | code |
# | --------- | ---- |
# | left      | -203 |
# | right     | -205 |
# | up        | -204 |
# | down      | -206 |
# | backspace | -300 |
# | pgup      | -207 |
# | pgdwn     | -208 |
# | del       | -102 |
# | tab       | -301 |
# | esc       | -1   |


def crapInput(screen):
    charecters = ""
    while True:
        ev = screen.get_key()
        print(ev)
        if ev == ord(";"):
            screen.close()
            main()
        elif ev == -300:
            charecters = charecters[:-1]
            screen.print_at(charecters+" ", 5, 3, 6)
            screen.refresh()
        elif ev != None and ev not in [-203 ,-205 ,-204 ,-206 ,-300 ,-207 ,-208 ,-102 ,-301 ,-1]:
            charecters = charecters+chr(ev)
            screen.print_at(charecters, 5, 3, 6)
            screen.refresh()
    return charecters


def main():
    print("hello world!")
    Screen.wrapper(adder)


main()
