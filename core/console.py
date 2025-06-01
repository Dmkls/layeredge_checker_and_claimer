import curses
import time
import os

ASCII_LOGO = [
    "██╗      █████╗ ██╗   ██╗███████╗██████╗ ███████╗██████╗  ██████╗ ███████╗",
    "██║     ██╔══██╗╚██╗ ██╔╝██╔════╝██╔══██╗██╔════╝██╔══██╗██╔════╝ ██╔════╝",
    "██║     ███████║ ╚████╔╝ █████╗  ██████╔╝█████╗  ██║  ██║██║  ███╗█████╗  ",
    "██║     ██╔══██║  ╚██╔╝  ██╔══╝  ██╔══██╗██╔══╝  ██║  ██║██║   ██║██╔══╝  ",
    "███████╗██║  ██║   ██║   ███████╗██║  ██║███████╗██████╔╝╚██████╔╝███████╗",
    "╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚═════╝  ╚═════╝ ╚══════╝",
]

MAIN_MENU_OPTIONS = ["Чекер", "Клеймер", "Выход"]
CLAIMER_OPTIONS = ["Gate", "Kucoin", "HashKey Global", "HTX", "Назад"]

def clear_line(stdscr, y):
    stdscr.move(y, 0)
    stdscr.clrtoeol()
    stdscr.refresh()

def draw_logo_animation(stdscr, logo_lines, delay=0.05):
    stdscr.clear()
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)

    h, w = stdscr.getmaxyx()
    start_y = h // 2 - len(logo_lines) // 2 - 1

    for i, line in enumerate(logo_lines):
        x = w // 2 - len(line) // 2
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(start_y + i, x, line)
        stdscr.attroff(curses.color_pair(1))
        stdscr.refresh()
        time.sleep(delay)

    subtitle = "claimer & checker"
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(start_y + len(logo_lines) + 1, w // 2 - len(subtitle) // 2, subtitle)
    stdscr.attroff(curses.color_pair(1))
    stdscr.refresh()
    time.sleep(1.5)

    subtitle = "tg.com/povedalcrypto"
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(start_y + len(logo_lines) + 1, w // 2 - len(subtitle) // 2, subtitle)
    stdscr.attroff(curses.color_pair(1))
    stdscr.refresh()
    time.sleep(2.5)

    clear_line(stdscr, start_y + len(logo_lines) + 1)

    subtitle = "claimer & checker"
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(start_y + len(logo_lines) + 1, w // 2 - len(subtitle) // 2, subtitle)
    stdscr.attroff(curses.color_pair(1))
    stdscr.refresh()
    time.sleep(1.5)

    for i in reversed(range(len(logo_lines) + 2)):
        y = start_y + i
        stdscr.move(y, 0)
        stdscr.clrtoeol()
        stdscr.refresh()
        time.sleep(0.03)

def draw_menu(stdscr, selected_idx, options):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    for idx, item in enumerate(options):
        x = w // 2 - len(item) // 2
        y = h // 2 - len(options) // 2 + idx
        if idx == selected_idx:
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(y, x, item)
            stdscr.attroff(curses.A_REVERSE)
        else:
            stdscr.addstr(y, x, item)
    stdscr.refresh()

def menu_selector(stdscr, options):
    current_idx = 0
    while True:
        draw_menu(stdscr, current_idx, options)
        key = stdscr.getch()
        if key == curses.KEY_UP:
            current_idx = (current_idx - 1) % len(options)
        elif key == curses.KEY_DOWN:
            current_idx = (current_idx + 1) % len(options)
        elif key in [curses.KEY_ENTER, 10, 13]:
            return current_idx

def main(stdscr):
    h, w = stdscr.getmaxyx()
    curses.curs_set(0)
    draw_logo_animation(stdscr, ASCII_LOGO)

    while True:
        main_choice_idx = menu_selector(stdscr, MAIN_MENU_OPTIONS)
        main_choice = MAIN_MENU_OPTIONS[main_choice_idx]

        stdscr.clear()

        if main_choice == "Клеймер":
            while True:
                platform_idx = menu_selector(stdscr, CLAIMER_OPTIONS)
                platform_choice = CLAIMER_OPTIONS[platform_idx]
                if platform_choice == "Назад":
                    break
                msg = f"Запуск клеймера на {platform_choice}..."
                stdscr.clear()
                stdscr.addstr(h // 2, w // 2 - len(msg) // 2, msg)
                stdscr.refresh()
                time.sleep(1.5)
                return platform_choice
        else:
            stdscr.addstr(h // 2, w // 2 - len(main_choice) // 2, main_choice)
            stdscr.refresh()
            time.sleep(1)

            return main_choice

def init_console():
    os.system("cls" if os.name == "nt" else "clear")
    return curses.wrapper(main)

if __name__ == "__main__":
    init_console()
