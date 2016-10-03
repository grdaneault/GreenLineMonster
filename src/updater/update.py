import argparse
import csv

import requests

from src.models import Game

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', dest='file', default='-',
                    help='the location of the file to write after downloading the schedule')
parser.add_argument('-u', '--url', dest='url',
                    default='http://mlb.mlb.com/ticketing-client/csv/EventTicketPromotionPrice.tiksrv?team_id=111&home_team_id=111&display_in=singlegame&ticket_category=Tickets&site_section=Default&sub_category=Default&leave_empty_games=true&event_type=T&event_type=Y',
                    help='The location containing the CSV for home games')

CSV_START_DATE = 'START DATE ET'
CSV_START_TIME = 'START TIME ET'
CSV_END_DATE = 'END DATE ET'
CSV_END_TIME = 'END TIME ET'
CSV_SUBJECT = 'SUBJECT'

indices = {
    CSV_START_DATE: 0,
    CSV_START_TIME: 2,
    CSV_END_DATE: 6,
    CSV_END_TIME: 9,
    CSV_SUBJECT: 3
}




def main():
    args = parser.parse_args()
    schedule = requests.get(args.url)
    rows = schedule.text.strip().split('\n')
    reader = csv.reader(rows)

    games = []
    headers = True
    for row in reader:
        if headers:
            headers = False
            for i in range(len(row)):
                indices[row[i]] = i
        else:
            start_date = row[indices[CSV_START_DATE]]
            start_time = row[indices[CSV_START_TIME]]
            end_date = row[indices[CSV_END_DATE]]
            end_time = row[indices[CSV_END_TIME]]
            description = row[indices[CSV_SUBJECT]]

            if start_date and start_time and end_date and end_time:
                # Some times may be TBD.  If the game details aren't known we don't care about this game
                game = Game(start_date, start_time, end_date, end_time, description)
                games.append(game)
                print(game)
    print(games)


if __name__ == '__main__':
    main()
