#!/usr/bin/python

import curses
import curses.textpad
import re

stdscr = curses.initscr()
#curses.start_color()
# don't echo key strokes on the stdscr
curses.noecho()
# read keystrokes instantly, without waiting for enter to ne pressed
curses.cbreak()
# enable keypad mode
stdscr.keypad(1)
stdscr.clear()
stdscr.refresh()


def maketextbox(h, w, y, x, title="", value=""):
    nw = curses.newwin(h, w, y + 1, x)
    txtbox = curses.textpad.Textbox(nw)
    nw.addstr(0, 0, value)
    stdscr.addstr(y, x, title, curses.A_UNDERLINE)
    replacetext(nw, value)
    return txtbox


def makewindow(h, w, y, x, title="", value=""):
    nw = curses.newwin(h, w, y + 1, x)
    nw.addstr(0, 0, value)
    replacetext(nw, value)
    return nw


def replacetext(win, text):
    win.clear()
    y, x = win.getmaxyx()
    win.addstr(0, 0, text[:x - 1])
    win.refresh()
    stdscr.refresh()

h, w = stdscr.getmaxyx()

eb_pattern = maketextbox(1, w, 0, 0, "pattern", r"(?ism)(\w+).*?")
eb_repl = maketextbox(1, w, 2, 0, "repl", r"*\1*")
eb_string = maketextbox(4, w, 4, 0, "string", "What is love?")

tb_findall = makewindow(4, w, 12, 0, "findall", "findall groups go here")
tb_sub = makewindow(4, w, 18, 0, "sub", "sub results go here")
tb_findall_e = makewindow(1, w, 24, 0, "findall Exception", "findall exceptions")
tb_sub_e = makewindow(1, w, 26, 0, "sub Exception", "sub exceptions")

stdscr.refresh()

e = None
try:
    while True:

        stdscr.refresh()
        
        s_pattern = eb_pattern.edit()
        s_repl = eb_repl.edit()
        s_string = eb_string.edit()

        s_findall = ""
        s_sub = ""

        try:
            s_findall = repr(re.findall(s_pattern, s_string))
        except Exception, e:
            replacetext(tb_findall_e, repr(e))  # +':'+str(e))

        try:
            s_sub = repr(re.sub(s_pattern, s_repl, s_string))
        except Exception, e:
            replacetext(tb_sub_e, repr(e))  # +':'+str(e))

        replacetext(tb_findall, s_findall)
        replacetext(tb_sub, s_sub)
        stdscr.refresh()

except Exception, e:
    pass

curses.endwin()
print str(e) + repr(e)
