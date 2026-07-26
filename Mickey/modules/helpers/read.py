from config import OWNER_USERNAME, SUPPORT_GRP
from Mickey import MickeyBot


def _table(rows):
    width = max(len(cmd) for cmd, _ in rows) + 3
    lines = [f"{'Command':<{width}}Description"]
    for cmd, desc in rows:
        lines.append(f"{cmd:<{width}}{desc}")
    return "<pre>" + "\n".join(lines) + "</pre>"


START = f"""👋 Hey, I am <b>{MickeyBot.name}</b>
An AI based chatbot that learns from your group and replies automatically.

<b>Usage:</b> /chatbot [on/off]
Hit the <b>Help</b> button below for the full command list."""

HELP_READ = f"""<b>User Commands</b>
Commands available to all members of the chat.

<blockquote expandable><b>Chatbot</b>
{_table([("/chatbot", "Enable/disable the chatbot")])}</blockquote>

<blockquote expandable><b>Tools</b>
Tap the Tools button below.</blockquote>

© @{OWNER_USERNAME}"""

TOOLS_DATA_READ = f"""<b>Tools</b>
{_table([
    ("/repo", f"Get the source code of {MickeyBot.name}"),
    ("/ping", f"Check the ping of {MickeyBot.name}"),
    ("/id", "Get your user, chat & msg ID"),
])}

© @{OWNER_USERNAME}"""

CHATBOT_READ = f"""<b>Chatbot</b>
{_table([("/chatbot", "Enable/disable the chatbot")])}

<blockquote>Works in groups and in private.</blockquote>

© @{OWNER_USERNAME}"""

SOURCE_READ = f"""<b>Source Code</b>
The source code of <a href="https://t.me/{MickeyBot.username}">{MickeyBot.name}</a> is given below.
Please fork the repo and give it a star ✯

Here is the <a href="https://github.com/Devarora-0981/Mickey">source code</a>.
If you face any problem, contact the <a href="https://t.me/{SUPPORT_GRP}">support chat</a>.

© @{OWNER_USERNAME}"""

ADMIN_READ = "<b>Admins</b>\nComing soon."

ABOUT_READ = f"""<b>About</b>
<a href="https://t.me/{MickeyBot.username}">{MickeyBot.name}</a> is an AI based chatbot.
It replies automatically to users and helps activate learning in your groups.
Written in <a href="https://www.python.org">Python</a> with <a href="https://www.mongodb.com">MongoDB</a> as a database.

Use the buttons below for basic help and info about {MickeyBot.name}."""
