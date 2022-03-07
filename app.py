
import os
import time
import datetime
import urllib.request
from pathlib import Path
from slack_bolt import App
from dotenv import load_dotenv
from calendar import WEDNESDAY
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.socket_mode import SocketModeHandler

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_APP_TOKEN = os.getenv('SLACK_APP_TOKEN')

app = App(token=SLACK_BOT_TOKEN)

def get_ts_from():
    today = datetime.date.today()
    days_since_last_wednesday = (today.weekday() - WEDNESDAY) % 7
    seconds_since_last_wednesday = days_since_last_wednesday * 24 * 60 * 60

    return str(round(time.time() - seconds_since_last_wednesday))

@app.command('/download')
def download_memes(ack, respond, command):
    ack()

    try:
        result = app.client.files_list(
            token=SLACK_BOT_TOKEN,
            channel='CTSDZBQBW',
            ts_from=get_ts_from()
        )

        respond(f'Starting file download...\nFiles: {len(result["files"])}')
        
        for image in result['files']:
            file_name = image['name']
            if not os.path.isfile(f'./images/{file_name}'):
                url = image['url_private']

                req = urllib.request.Request(url)
                req.add_header('Authorization', f'Bearer {SLACK_BOT_TOKEN}')
                content=urllib.request.urlopen(req).read()

                with open(f'./images/{file_name}', 'wb') as handler:
                    handler.write(content)
                
                respond(f'{file_name} downloaded.')
            else:
                respond(f'The file {file_name} already exists.')

    except SlackApiError as e:
        respond(f'Download failed: {e}')

if __name__ == '__main__':
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
