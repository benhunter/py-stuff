# https://stackoverflow.com/questions/2515244/how-to-scroll-text-in-python-curses-subwindow

import curses


def main(stdscr):
    mypad = curses.newpad(40, 60)
    mypad_pos = 0

    mypad.refresh(mypad_pos, 0, 5, 5, 10, 60)

    k = 0

    # input loop
    while k != ord('q'):
        if k == curses.KEY_DOWN:
            mypad_pos += 1
            mypad.refresh(mypad_pos, 0, 5, 5, 10, 60)
        elif k == curses.KEY_UP:
            mypad_pos -= 1
            mypad.refresh(mypad_pos, 0, 5, 5, 10, 60)

        k = stdscr.getch()


if __name__ == '__main__':
    curses.wrapper(main)
