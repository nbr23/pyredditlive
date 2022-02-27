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
    config = None
    if not os.path.isfile(config_path):
        print("Config file '%s' not found." % config_path)
        return None
    with open(config_path) as configfile:
        config = yaml.load(configfile, Loader=yaml.SafeLoader)
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
    elif update.get("type") == "embeds_ready":
        for embed in update.get("payload", {}).get("mobile_embeds", []):
            description = embed.get("description", "")
            title = embed.get("title", "")
            html = embed.get("html")
            if html is not None:
                print(f"POSTING {title}\n{description}\n{html}")
                requests.get(
                    f'https://api.telegram.org/{config["telegram_bot"]}/sendMessage?chat_id={config.get("telegram_chat_id")}&text={urllib.parse.quote_plus(title)}'
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
