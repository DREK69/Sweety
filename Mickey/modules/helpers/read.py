from config import OWNER_USERNAME, SUPPORT_GRP
from Mickey import MickeyBot

START_HTML = f"""
<h2>👋 Hey, I am {MickeyBot.name}</h2>
<p>An AI based chatbot that learns from your group and replies automatically.</p>
<hr>
<p><b>Usage:</b> /chatbot [on/off]</p>
<p>Hit the <b>Help</b> button below for the full command list.</p>
"""

HELP_HTML = f"""
<h2>User Commands</h2>
<p>Commands available to all members of the chat.</p>
<details open>
<summary><b>Chatbot</b></summary>
<table>
<tr><th>Command</th><th>Description</th></tr>
<tr><td>/chatbot</td><td>Enable or disable the learning chatbot for this group.</td></tr>
</table>
</details>
<details>
<summary><b>Tools</b></summary>
<p>Tap the Tools button below.</p>
</details>
<hr>
<p>© @{OWNER_USERNAME}</p>
"""

TOOLS_DATA_HTML = f"""
<h2>Tools</h2>
<table>
<tr><th>Command</th><th>Description</th></tr>
<tr><td>/repo</td><td>Get the source code of {MickeyBot.name}.</td></tr>
<tr><td>/ping</td><td>Check the ping of {MickeyBot.name}.</td></tr>
<tr><td>/id</td><td>Get your user ID, chat ID and message ID in one message.</td></tr>
</table>
<hr>
<p>© @{OWNER_USERNAME}</p>
"""

CHATBOT_HTML = f"""
<h2>Chatbot</h2>
<table>
<tr><th>Command</th><th>Description</th></tr>
<tr><td>/chatbot</td><td>Enable or disable the chatbot.</td></tr>
</table>
<blockquote>Note: this command only works in groups.</blockquote>
<hr>
<p>© @{OWNER_USERNAME}</p>
"""

SOURCE_HTML = f"""
<h2>Source Code</h2>
<p>The source code of <a href="https://t.me/{MickeyBot.username}">{MickeyBot.name}</a> is given below.</p>
<p>Please fork the repo and give it a star ✯</p>
<hr>
<p>Here is the <a href="https://github.com/Devarora-0981/Mickey">source code</a>.</p>
<p>If you face any problem, contact the <a href="https://t.me/{SUPPORT_GRP}">support chat</a>.</p>
<hr>
<p>© @{OWNER_USERNAME}</p>
"""

ADMIN_HTML = "<h2>Admins</h2><p>Coming soon.</p>"

ABOUT_HTML = f"""
<h2>About</h2>
<p><a href="https://t.me/{MickeyBot.username}">{MickeyBot.name}</a> is an AI based chatbot.</p>
<p>It replies automatically to users and helps activate learning in your groups.</p>
<p>Written in <a href="https://www.python.org">Python</a> with <a href="https://www.mongodb.com">MongoDB</a> as a database.</p>
<hr>
<p>Use the buttons below for basic help and info about {MickeyBot.name}.</p>
"""

START = START_HTML
HELP_READ = HELP_HTML
TOOLS_DATA_READ = TOOLS_DATA_HTML
CHATBOT_READ = CHATBOT_HTML
ADMIN_READ = ADMIN_HTML
ABOUT_READ = ABOUT_HTML
SOURCE_READ = SOURCE_HTML
