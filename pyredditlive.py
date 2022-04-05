#!/usr/bin/env python3

import asyncio
import websockets
import requests
import json
import sys
import os
import yaml
import urllib


def load_config(config_path):
    config = {}

    if os.path.exists(config_path):
        with open(config_path) as configfile:
            config = yaml.load(configfile, Loader=yaml.SafeLoader)
    if 'PYRL_TELEGRAM_BOT' in os.environ:
        config['telegram_bot'] = os.environ['PYRL_TELEGRAM_BOT']
    if 'PYRL_TELEGRAM_CHAT_ID' in os.environ:
        config['telegram_chat_id'] = os.environ['PYRL_TELEGRAM_CHAT_ID']

    if 'telegram_bot' not in config or 'telegram_chat_id' not in config:
        raise Exception("No configuration file found or environment variable set")

    return config


def get_ws_url(url):
    res = (
        requests.get(f"{url}about.json", headers={"User-agent": "Mozilla/5.0"})
        .json()
        .get("data", {})
    )
    if res.get("state") == "live":
        return res.get("websocket_url")
    raise Exception(f"Livethread state is {res.get('state')}")


def post_update(update, config):
    if update.get("type") == "update":
        body = update.get("payload", {}).get("data", {}).get("body")
        if body is not None:
            print(f"POSTING {body}")
            requests.get(
                f'https://api.telegram.org/{config["telegram_bot"]}/sendMessage?chat_id={config.get("telegram_chat_id")}&text={urllib.parse.quote_plus(body)}'
            )


async def livethread(url, config):
    while True:
        ws_url = get_ws_url(url)
        try:
            async with websockets.connect(ws_url) as websocket:
                requests.get(
                    f'https://api.telegram.org/{config["telegram_bot"]}/sendMessage?chat_id={config.get("telegram_chat_id")}&text={urllib.parse.quote_plus("Connected to "+ws_url)}'
                )
                print(f"Connected to {ws_url}")
                while True:
                    update = await websocket.recv()
                    print(f"RAW JSON:\n{update}")
                    post_update(json.loads(update), config)
        except websockets.ConnectionClosed:
            continue


def main():
    config = load_config("./config.yml")
    asyncio.run(livethread(sys.argv[1], config))


if __name__ == "__main__":
    sys.exit(main())
