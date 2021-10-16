import arrow
import csv

import requests
from dateutil import tz

class Game(object):
    EXPECTED_DATE_FORMAT = 'MM/DD/YY HH:mm A'

    def __init__(self, start_date, start_time, end_date, end_time, description):
        self.start = arrow.get('%s %s' % (start_date, start_time), Game.EXPECTED_DATE_FORMAT, tzinfo=tz.gettz('US/Eastern'))
        self.start_extended = self.start.replace(hours=-4)
        self.end = arrow.get('%s %s' % (end_date, end_time), Game.EXPECTED_DATE_FORMAT, tzinfo=tz.gettz('US/Eastern'))
        self.end_extended = self.end.replace(hours=+4)
        self.description = description

    def __str__(self):
        return "%s: %s - %s" % (self.description, self.start.format('M/D/YY h:mm'), self.end.format('h:mm a'))

    def overlaps(self, time):
        return self.start_extended < time < self.end_extended

    def same_day(self, time):
        return self.start.date() == time.date() and time < self.end_extended

    __repr__ = __str__


def should_add_event(start_date, start_time, end_date, end_time, description):
    # Some times may be TBD.  If the event details aren't known we don't care about this event
    if not start_date or not start_time or not end_date or not end_time:
        return False

    # Filter out noise like tours and graduations so the site doesn't just perpetually show it's gameday
    for banned_keyword in Schedule.BANNED_EVENT_KEYWORDS:
        if banned_keyword in description:
            return False

    return True


class Schedule(object):
    CSV_START_DATE = 'START DATE'
    CSV_START_TIME = 'START TIME ET'
    CSV_END_DATE = 'END DATE'
    CSV_END_TIME = 'END TIME ET'
    CSV_SUBJECT = 'SUBJECT'
    BANNED_EVENT_KEYWORDS = [
        "Tour",
        "Parking",
        "NWE Test",
        "Test Event",
        "Cocktail Party",
        "Commencement",
        "NU "  # NU College of Professional Studies
    ]

    def __init__(self, url):
        self.games = []
        self.url = url
        self.last_updated = None
        self.reload()

    def current_game(self):
        now = arrow.now('US/Eastern')
        current = list(filter(lambda game: game.overlaps(now), self.games))
        if current:
            return current[0]
        return None

    def todays_game(self):
        now = arrow.now('US/Eastern')
        today = list(filter(lambda game: game.same_day(now), self.games))
        if today:
            return today[0]
        return None

    def reload(self):
        schedule = requests.get(self.url)
        rows = schedule.text.strip().split('\n')
        reader = csv.reader(rows)

        games = []
        indices = {}
        headers = True
        for row in reader:
            if headers:
                headers = False
                for i in range(len(row)):
                    indices[row[i]] = i
            else:
                start_date = row[indices[Schedule.CSV_START_DATE]]
                start_time = row[indices[Schedule.CSV_START_TIME]]
                end_date = row[indices[Schedule.CSV_END_DATE]]
                end_time = row[indices[Schedule.CSV_END_TIME]]
                description = row[indices[Schedule.CSV_SUBJECT]].strip()

                if should_add_event(start_date, start_time, end_date, end_time, description):
                    game = Game(start_date, start_time, end_date, end_time, description)
                    games.append(game)

        self.games = games
        self.last_updated = arrow.now('US/Eastern')
