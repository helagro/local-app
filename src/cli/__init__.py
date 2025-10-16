from transducers.actuators.led import get_lamp
import sys, tty, termios


def run_cli():

    while True:
        char = getch()

        print(f"Pressed: {char}", end='\r\n')

        menu(char)
        if char == 'q':
            break


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)  # or tty.setraw(fd) for true raw mode
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def menu(char: str) -> None:
    match char:
        case '8':
            get_lamp('red').on()
        case '9':
            get_lamp('blue').toggle()
        case _:
            print("Invalid input", end='\r\n')
