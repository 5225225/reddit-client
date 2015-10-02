import os
import uuid
import subprocess
import webserver

import praw

scope = [
    "creddits",
    "edit",
    "flair",
    "history",
    "identity",
    "modconfig",
    "modcontributors",
    "modflair",
    "modlog",
    "modothers",
    "modposts",
    "modself",
    "modwiki",
    "mysubreddits",
    "privatemessages",
    "read",
    "report",
    "save",
    "submit",
    "subscribe",
    "vote",
    "wikiedit",
    "wikiread",
]

def auth(reddit):

    reddit.set_oauth_app_info(
        client_id="wXs3zvzvVEj0nw",
        redirect_uri="http://localhost:8888/authorize_callback",
        client_secret="what-the-hell-i-don't-have-a-client-secret",
    )


    have_creds = os.path.exists("refresh-token")

    if have_creds:
        refresh_token = open("refresh-token").read()

        access_information = {}

        access_information["refresh_token"] = refresh_token
        access_information["access_token"] = "refresh-me"

        access_information["scope"] = set(scope)

        try:
            reddit.set_access_credentials(**access_information)
        except praw.errors.HTTPException:
            print("Something went wrong. Maybe your access token was revoked")

        print("Logged in using stored creds")
    else:
        state = uuid.uuid4()

        url = reddit.get_authorize_url(state, ",".join(scope), True)

        subprocess.call(["firefox", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)

        try:
            code = webserver.get_code()
        except AssertionError:
            print("Something went wrong")
            print()
            print("You may have clicked decline. By the way, it's hard for me to")
            print("work if you don't give me permission.")
            sys.exit(0)

        access_information = reddit.get_access_information(code)

        with open("refresh-token", "w") as f:
            f.write(access_information["refresh_token"])

        print("Made creds file")

