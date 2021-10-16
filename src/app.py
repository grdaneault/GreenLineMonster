from flask import Flask, render_template, abort, request
import random

from models import Schedule


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.SiteConfig')
    schedule = Schedule(app.config.get('SCHEDULE_URL'))

    def message_for_state(state):
        return random.choice(app.config.get('MESSAGES')[state])

    def analytics_id():
        ids = app.config.get('ANALYTICS_IDS')
        if request.host in ids:
            return ids[request.host]
        else:
            return ids['default']

    @app.route('/')
    def index():
        state = app.config.get('STATE_OKAY')
        subtitle = ''

        current_game = schedule.current_game()
        if current_game is not None:
            state = app.config.get('STATE_TROUBLE')
            subtitle = str(current_game)
        else:
            game_today = schedule.todays_game()
            if game_today is not None:
                state = app.config.get('STATE_WARN')
                subtitle = str(game_today)

        return render_template(
            'index.html',
            site_name=app.config.get('SITE_NAME'),
            analytics_id=analytics_id(),
            state=state,
            image=app.config.get('IMAGES')[state],
            message=message_for_state(state),
            subtitle=subtitle
        )

    @app.route('/test/<state>')
    def index_override(state):
        if state in app.config.get('ALLOWED_STATES'):
            return render_template(
                'index.html',
                site_name=app.config.get('SITE_NAME'),
                analytics_id=analytics_id(),
                state=state,
                image=app.config.get('IMAGES')[state],
                message=message_for_state(state),
                subtitle="Doin a test."
            )
        else:
            return abort(400)

    @app.route('/schedule')
    def get_schedule():
        return render_template(
            'schedule.html',
            site_name=app.config.get('SITE_NAME'),
            analytics_id=analytics_id(),
            games=schedule.games,
            last_updated=schedule.last_updated
        )

    @app.route('/update')
    def update_schedule():
        if 'X-Real-IP' in request.headers:
            remote = request.headers['X-Real-IP'].split(',')[0]
        else:
            remote = "127.0.0.1"

        if remote == "127.0.0.1":
            schedule.reload()
            return render_template(
                'schedule.html',
                site_name=app.config.get('SITE_NAME'),
                analytics_id=analytics_id(),
                games=schedule.games,
                last_updated=schedule.last_updated
            )
        return abort(404)

    return app


if __name__ == '__main__':
    create_app().run()
