import atexit
import curses
import datetime
import sys
import time
import warnings

import praw

import authenticate
import util

warnings.simplefilter("ignore", ResourceWarning)
warnings.simplefilter("ignore", ImportWarning)
# It's not good to ignore warnings, but I need to keep the screen clear unless
# there is an issue. Maybe switch to logging them to a file?

def resize_screen():
    global needs_refreshing

    global win_status_bar
    global list_view_pad
    global command_bar

    curses.update_lines_cols()

    win_status_bar = curses.newwin(1, curses.COLS)
    list_view_pad = curses.newpad(300 + 2*3, curses.COLS)
    # The length of posts is not always going to be 100, as stickies are returned
    # separately, so it's 100 + number of stickies.

    command_bar = curses.newwin(1, curses.COLS, curses.LINES-1, 0)

    
    needs_refreshing = ["viewing", "status-bar", "list-view"]


def readcommand(disp, prompt):
    disp.clear()
    disp.move(0, 0)

    disp.addstr(prompt)
    disp.refresh()
    curses.echo()
    cmd = disp.getstr()
    curses.noecho()
    return cmd

def refresh_list_view(list_view_pad, subreddit):
    global lenposts
    posts = util.refresh_subreddit(subreddit, sort, filter_time)
    lenposts = len(posts)
    list_view_pad.clear()
    list_view_pad.move(0,0)
    for i, post in enumerate(posts):
        pos = i * 3

        title = post.title[:curses.COLS - len(post.domain) - 4]

        line1 = "{} ({})".format(title, post.domain)

        list_view_pad.addstr(pos, 1, line1)


        points = post.score
        author = post.author.name

        comments = str(post.num_comments)
        if post.num_comments == 1:
            comments += " comment"
        else:
            comments += " comments"

        nowdate = datetime.datetime.fromtimestamp(time.time())
        postdate = datetime.datetime.fromtimestamp(post.created_utc)

        ago = postdate - nowdate

        ago = util.humanify_td(ago)

        line2 = "{} points submitted {} ago by {} {}".format(points, ago, author,
        comments)

        list_view_pad.addstr(pos + 1, 1, line2)

def refresh_status_bar(window, subreddit, user, screen):
    window.clear()
    window.move(0,0)
    if screen == "post-list":
        window.addstr("/r/{}".format(subreddit))
    
    username = "/u/{}".format(user.name)
    karma = "({}·{})".format(user.link_karma, user.comment_karma)
    msgbox = "[{}]".format(len(list(reddit.get_unread())))

    totallen = len(username) + len(karma) + len(msgbox) + 3

    window.move(0, curses.COLS - totallen)

    window.addstr(username + " ", curses.A_UNDERLINE)
    window.addstr(karma + " ")
    window.addstr(msgbox, curses.A_BOLD)


def shutdown(scr):
    curses.nocbreak()
    scr.keypad(0)
    curses.echo()
    curses.curs_set(2)
    curses.endwin()

reddit = praw.Reddit(
    "reddit CLI /u/5225225"
)

DIST_FROM_EDGE_SCROLL = 3


authenticate.auth(reddit)

scr = curses.initscr()
curses.noecho()
curses.cbreak()
scr.keypad(1)
curses.curs_set(0)

atexit.register(shutdown, scr)

# This avoids having to wrap everything in a main function, but still allows
# us to recover from any error

win_status_bar = curses.newwin(1, curses.COLS)
list_view_pad = curses.newpad(300 + 2*3, curses.COLS)
lenposts = 0
# The length of posts is not always going to be 100, as stickies are returned
# separately, so it's 100 + number of stickies.

command_bar = curses.newwin(1, curses.COLS, curses.LINES-1, 0)

screen = "post-list"
sort = "hot"
filter_time = "all"
index = 0
viewing = 0
# Can be "front", "post-list", "comments"

subreddit = reddit.get_subreddit("redditdev")

needs_refreshing = ["viewing", "status-bar", "list-view"]


while True:
    if "list-view" in needs_refreshing:
        refresh_list_view(list_view_pad, subreddit)
        needs_refreshing.append("viewing")


    if "viewing" in needs_refreshing:
        if viewing > 0:
            list_view_pad.vline(viewing * 3 - 3, 0, " ", 9)
        if viewing < lenposts - 1:
            list_view_pad.vline(viewing * 3 + 3, 0, " ", 9)
        list_view_pad.vline(viewing * 3, 0, "|", 2)

        if (viewing*3 - index) > (curses.LINES - 3 - (DIST_FROM_EDGE_SCROLL * 3)):
            index += 3
        elif (viewing*3 - index) < DIST_FROM_EDGE_SCROLL * 3:
            index -= 3



        list_view_pad.refresh(index, 0, 1, 0, curses.LINES-2, curses.COLS)

    if "status-bar" in needs_refreshing:
        refresh_status_bar(win_status_bar, subreddit, reddit.get_me(), screen)
        win_status_bar.refresh()

    needs_refreshing = []

    if screen == "post-list":
        ch = command_bar.getch()
        if chr(ch) == "j":
            if viewing < lenposts - 1:
                viewing += 1
                needs_refreshing.append("viewing")

        if chr(ch) == "k":
            if 0 < viewing:
                viewing -= 1
                needs_refreshing.append("viewing")

        if chr(ch) == "r":
            subreddit_name = readcommand(command_bar, "/r/").decode("UTF-8")
            subreddit = reddit.get_subreddit(subreddit_name)
            index = 0
            viewing = 0

            needs_refreshing.append("list-view")
            needs_refreshing.append("status-bar")

        if ch == curses.KEY_RESIZE:
            resize_screen()
