import curses
from datetime import datetime, timedelta
import calendar


# Example tracking data (Day: Hours Tracked)
tracking_data = {1: 8, 2: 4, 3: 6, 5: 1, 8: 7, 12: 3, 15: 2, 18: 0, 20: 5}

def get_fill_char(hours):
    """Determine fill level based on hours tracked"""
    if hours >= 6:
        return "█"  # Fully tracked
    elif hours > 0:
        return "▒"  # Partially tracked
    else:
        return "·"  # Not tracked

def draw_calendar(stdscr, year, month):
    """Draws the calendar with tracking data"""
    stdscr.clear()
    curses.curs_set(0)  # Hide cursor
    height, width = stdscr.getmaxyx()

    title = f"{calendar.month_name[month]} {year}"
    stdscr.addstr(1, (width - len(title)) // 2, title, curses.A_BOLD)

    days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

    # Print days of the week
    for i, day in enumerate(days):
        stdscr.addstr(3, i * 4 + 2, day, curses.A_UNDERLINE)

    cal = calendar.monthcalendar(year, month)

    for row, week in enumerate(cal):
        for col, day in enumerate(week):
            x = col * 4 + 2
            y = row + 5  # Adjust for header

            if day == 0:
                stdscr.addstr(y, x, "   ")  # Empty spot
            else:
                char = get_fill_char(tracking_data.get(day, 0))
                stdscr.addstr(y, x, f"{day:2}{char}")

    stdscr.refresh()

def curses_cal(stdscr):
    """Main loop handling user input"""
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(False)  # Wait for user input
    stdscr.keypad(True)  # Enable arrow keys

    # Start with the current month and year
    now = datetime.now()
    year, month = now.year, now.month

    while True:
        draw_calendar(stdscr, year, month)

        key = stdscr.getch()

        if key == curses.KEY_RIGHT:
            month += 1
            if month > 12:
                month = 1
                year += 1
        elif key == curses.KEY_LEFT:
            month -= 1
            if month < 1:
                month = 12
                year -= 1
        elif key == ord('q'):  # Quit
            break
