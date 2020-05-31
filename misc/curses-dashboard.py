import curses

stdscr = None


def init():
    stdscr = curses.initscr()  # get the window object representing the entire screen
    curses.noecho()  # don't print chars that are pressed

    curses.cbreak()  # react to keys instantly without requiring Enter

    stdscr.keypad(True)  # enable processing of cursor or navigation keys ex: curses.KEY_LEFT


def end():
    # terminate curses application
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


# init()
# end() # still leaves the terminal in a weird state... :/

from curses import wrapper


def main(stdscr):
    stdscr.clear()

    # intentionally raise ZeroDivisionError:
    for i in range(10):
        v = i + 1
        stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10 / v))

    stdscr.refresh()
    stdscr.getkey()


wrapper(main)
