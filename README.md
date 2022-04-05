# pyredditlive

Fetch updates from reddit live threads and posts them on telegram

## Configuration

### Config.yml

Fill in your telegram bot ID and chat ID in the config.yml file

### Environment Variables

You can also set the telegram variables with environment variables:
```
PYRL_TELEGRAM_BOT='botXXXXXXXXXXXXx' # Bot token of your telegram bot
PYRL_TELEGRAM_CHAT_ID='' # chat_id of the contact or group to send the messages to

```

## Usage

`./pyredditlive.py LIVE_THREAD_URL`

## Docker

Pull the image:
`docker pull nbr23/pyredditlive:latest`

Run:
`docker run --env PYRL_TELEGRAM_CHAT_ID=XXXXX --env PYRL_TELEGRAM_BOT=XXXX:XXXXXXXX nbr23/pyredditlive https://www.reddit.com/live/XXXXXXXXXXXXX/`

Or mapping a local config file:

`docker run -v $PWD/config.yml:/usr/src/app/config.yml nbr23/pyredditlive https://www.reddit.com/live/XXXXXXXXXXXXX/`