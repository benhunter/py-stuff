# https://stackoverflow.com/questions/2515244/how-to-scroll-text-in-python-curses-subwindow

# !/usr/bin/env python2.7
import curses

# content - array of lines (list)
mylines = ["Line {0} ".format(id) * 3 for id in range(1, 11)]

import pprint

pprint.pprint(mylines)


def main(stdscr):
    hlines = begin_y = begin_x = 5;
    wcols = 10
    # calculate total content size
    padhlines = len(mylines)
    padwcols = 0
    for line in mylines:
        if len(line) > padwcols: padwcols = len(line)
    padhlines += 2;
    padwcols += 2  # allow border
    stdscr.addstr("padhlines " + str(padhlines) + " padwcols " + str(padwcols) + "; ")
    # both newpad and subpad are <class '_curses.curses window'>:
    mypadn = curses.newpad(padhlines, padwcols)
    mypads = stdscr.subpad(padhlines, padwcols, begin_y, begin_x + padwcols + 4)
    stdscr.addstr(str(type(mypadn)) + " " + str(type(mypads)) + "\n")
    mypadn.scrollok(1)
    mypadn.idlok(1)
    mypads.scrollok(1)
    mypads.idlok(1)
    mypadn.border(0)  # first ...
    mypads.border(0)  # ... border
    for line in mylines:
        mypadn.addstr(padhlines - 1, 1, line)
        mypadn.scroll(1)
        mypads.addstr(padhlines - 1, 1, line)
        mypads.scroll(1)
        # time.sleep(1)
    mypadn.border(0)  # second ...
    mypads.border(0)  # ... border
    # refresh parent first, to render the texts on top
    # ~ stdscr.refresh()
    # refresh the pads next
    mypadn.refresh(0, 0, begin_y, begin_x, begin_y + hlines, begin_x + padwcols)
    mypads.refresh()
    mypads.touchwin()
    mypadn.touchwin()
    stdscr.touchwin()  # no real effect here
    # stdscr.refresh() # not here! overwrites newpad!
    mypadn.getch()
    # even THIS command erases newpad!
    # (unless stdscr.refresh() previously):
    stdscr.getch()


curses.wrapper(main)
