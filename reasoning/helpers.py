import curses

def input_with_unique_choices(message, choices, num_choices):
    stdscr = curses.initscr()
    curses.noecho()
    stdscr.keypad(True)
    cursor = 0
    KEY_UP = 259
    KEY_DOWN = 258
    KEY_ENTER = 10
    chosen_items = []
    for i in range(num_choices):
        stdscr.clear()
        stdscr.addstr(message + "\n")
        for j, choice in enumerate(choices):
            if j == cursor:
                stdscr.addstr("  > " + choice + "\n")
            else:
                stdscr.addstr("    " + choice + "\n")
        stdscr.refresh()
        while True:
            key = stdscr.getch()
            if key == KEY_UP:
                cursor = max(cursor - 1, 0)
            elif key == KEY_DOWN:
                cursor = min(cursor + 1, len(choices) - 1)
            elif key == KEY_ENTER:
                if choices[cursor] in chosen_items:
                    stdscr.addstr("You have already chosen this item. Please choose a different one.\n")
                    stdscr.refresh()
                    continue
                chosen_items.append(choices[cursor])
                choices.remove(choices[cursor])
                break
            stdscr.clear()
            stdscr.addstr(message + "\n")
            for j, choice in enumerate(choices):
                if j == cursor:
                    stdscr.addstr("  > " + choice + "\n")
                else:
                    stdscr.addstr("    " + choice + "\n")
            stdscr.refresh()
    curses.echo()
    stdscr.keypad(False)
    curses.endwin()
    return chosen_items

def input_with_choices(message, choices):
    stdscr = curses.initscr()
    curses.noecho()
    stdscr.keypad(True)
    cursor = 0
    KEY_UP = 259
    KEY_DOWN = 258
    KEY_ENTER = 10
    stdscr.addstr(message + "\n")
    while True:
        for i, choice in enumerate(choices):
            if i == cursor:
                stdscr.addstr("  > " + choice + "\n")
            else:
                stdscr.addstr("    " + choice + "\n")
        stdscr.refresh()
        key = stdscr.getch()
        if key == KEY_UP:
            cursor = max(cursor - 1, 0)
        elif key == KEY_DOWN:
            cursor = min(cursor + 1, len(choices) - 1)
        elif key == KEY_ENTER:
            break
        stdscr.clear()
        stdscr.addstr(message + "\n")
    curses.echo()
    stdscr.keypad(False)
    curses.endwin()
    return choices[cursor]