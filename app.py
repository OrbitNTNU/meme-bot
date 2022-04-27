import os
import subprocess
import urllib.request
from pathlib import Path
from slack_bolt import App
from dotenv import load_dotenv
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.socket_mode import SocketModeHandler

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
APP_TOKEN = os.getenv('APP_TOKEN')
MEME_CHANNEL_ID = os.getenv('MEME_CHANNEL_ID')
SPONSOR_CHANNEL_ID = os.getenv('SPONSOR_CHANNEL_ID')

app = App(token=SLACK_BOT_TOKEN)


@app.command('/download-memes')
def download_memes(ack, respond, command):
    ack()

    try:
        result = app.client.files_list(
            token=SLACK_BOT_TOKEN,
            channel=MEME_CHANNEL_ID,
            count=1000,
            types='images'
        )

        respond(f'Starting file download...\nFiles: {len(result["files"])}')
        
        downloaded = 0
        
        CWD = os.path.dirname(os.path.abspath(__file__))
        
        for image in result['files']:
            my_file = os.path.join(f'{CWD}/memes/', f'{image["id"]}.{image["pretty_type"]}')
            if not os.path.isfile(my_file) and (my_file.split('.')[-1] == 'PNG' or my_file.split('.')[-1] == 'JPG' or my_file.split('.')[-1] == 'JPEG'):
                url = image['url_private']

                req = urllib.request.Request(url)
                req.add_header('Authorization', f'Bearer {SLACK_BOT_TOKEN}')
                content=urllib.request.urlopen(req).read()

                with open(my_file, 'wb') as handler:
                    handler.write(content)

                downloaded += 1

            respond(f'Download complete\nDownloaded {downloaded}/{len(result["files"])} files.')
        respond('Starting resizing')
        subprocess.call(f'{CWD}/resize-images.sh')
        respond('Resize complete')
            
    except SlackApiError as e:
        respond(f'Download failed: {e}')


@app.command('/download-sponsors')
def download_sponsors(ack, respond, command):
    ack()

    try:
        result = app.client.files_list(
                token=SLACK_BOT_TOKEN,
                channel=SPONSOR_CHANNEL_ID,
                count=1000,
                types='images'
                )
        
        CWD = os.path.dirname(os.path.abspath(__file__))
        directory = f'{CWD}/sponsors'

        respond('Removing existing files')
        for f in os.listdir(directory):
            os.remove(os.path.join(directory, f))
        respond('Done!')
        
        downloaded = 0
        
        respond(f'Starting file download...\nFiles: {len(result["files"])}')
        
        for image in result['files']:
            my_file = os.path.join(f'{directory}', f'{image["name"]}')
            if not os.path.isfile(my_file):
                url = image['url_private']

                req = urllib.request.Request(url)
                req.add_header('Authorization', f'Bearer {SLACK_BOT_TOKEN}')
                content=urllib.request.urlopen(req).read()

                with open(my_file, 'wb') as handler:
                    handler.write(content)

                downloaded += 1

            respond(f'Download complete\nDownloaded {downloaded}/{len(result["files"])} files.')
            respond('Starting resizing')
            subprocess.call(f'{CWD}/resize-images.sh')
            respond('Resize complete')
            
    except SlackApiError as e:
        respond(f'Download failed: {e}')

if __name__ == '__main__':
    SocketModeHandler(app, APP_TOKEN).start()
