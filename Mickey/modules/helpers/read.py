from config import OWNER_USERNAME
from Mickey import MickeyBot

START = f"""Hey, I am {MickeyBot.name}
An AI based chatbot that learns from your group and replies automatically.

Usage: /chatbot [on/off]
Tap Help & Cmds below for the full command list."""

HELP_READ = f"""User Commands

/chatbot — Enable or disable the chatbot for this chat.

© @{OWNER_USERNAME}"""

CHATBOT_READ = f"""Chatbot

/chatbot — Enable or disable the chatbot.
Works in groups and in private.

Tools

/repo — Get the source code of {MickeyBot.name}.
/ping — Check the ping of {MickeyBot.name}.
/id — Get your user, chat and message ID.

© @{OWNER_USERNAME}"""

SOURCE_READ = f"""Source Code

The source code of {MickeyBot.name} is given below.
Please fork the repo and give it a star.

contact puppy

© @{OWNER_USERNAME}"""

