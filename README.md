# Meme Screen Bot

Slackbot used to download memes from the meme channel.

## Development

### Built with

- [Python](https://www.python.org/)
- [bolt-python](https://github.com/slackapi/bolt-python)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

### Installation

```bash
pip install slack_bolt
pip install python-dotenv
```

### Environment variables

The following environment variables need to be set:

```text
SLACK_BOT_TOKEN
APP_TOKEN
```

If you are running locally, they can be set by putting them in a `.env` file at the root of the project.

### Running locally

```bash
python3 <filename.py>
```

### Hosting

This project will be hosted locally on a Raspberry Pi.
