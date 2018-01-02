class SiteConfig(object):
    SCHEDULE_URL = 'http://www.ticketing-client.com/ticketing-client/csv/EventTicketPromotionPrice.tiksrv?team_id=111&home_team_id=111&display_in=singlegame&ticket_category=Tickets&site_section=Default&sub_category=Default&leave_empty_games=true&event_type=T'
    SITE_NAME = 'ARE RED SOX FANS FUCKING UP THE GREEN LINE?'

    STATE_OKAY = 'okay'
    STATE_WARN = 'warn'
    STATE_TROUBLE = 'trouble'

    ALLOWED_STATES = [STATE_OKAY, STATE_WARN, STATE_TROUBLE]

    IMAGES = {
        STATE_OKAY: 't.svg',
        STATE_WARN: 't.svg',
        STATE_TROUBLE: 'socks.svg'
    }

    MESSAGES = {
        STATE_OKAY: ['NO WORSE THAN NORMAL', 'HMM... MIGHT BE OKAY', 'LOOKS FINE FROM HERE', 'IT\'S STILL THE GREEN LINE SO...', 'JUST YOUR EVERYDAY SHIT'],
        STATE_WARN: ['STORM ON THE HORIZON', 'YOU\'RE SAFE... FOR NOW', 'THE SOX FANS ARE COMING! THE SOX FANS ARE COMING!', 'IN YOUR FUTURE: REGRET'],
        STATE_TROUBLE: ['FUCK FUCK FUCK', 'NOT THIS SHIT AGAIN', 'UGH... HOW MUCH MORE \'TILL KENMORE?', 'CLOUDY WITH A CHANCE OF SARDINE TRAIN', 'FUCK, TODAY TOO?! HOW IS THAT POSSIBLE!?']
    }

    ANALYTICS_IDS = {
        'www.greenlinemonster.review': 'UA-83947538-1',
        'greenlinemonster.review': 'UA-83947538-1',
        'www.areredsoxfansfuckingupthegreenline.com': 'UA-83947538-2',
        'areredsoxfansfuckingupthegreenline.com': 'UA-83947538-2',
        'default': 'UA-83947538-2'
    }
