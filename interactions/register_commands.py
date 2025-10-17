import os
import httpx
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("DISCORD_APPLICATION_ID")
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# global command (can take ~1 hour to propagate globally; for instant testing use guild route)
url = f"https://discord.com/api/v10/applications/{APP_ID}/commands"
# or per-guild for instant: f"https://discord.com/api/v10/applications/{APP_ID}/guilds/{GUILD_ID}/commands"

commands = [
    {
        "name": "ping",
        "description": "Replies with pong.",
        "type": 1,  # CHAT_INPUT
    },
    {
        "name": "echo",
        "description": "Echoes back your message.",
        "type": 1,  
        "options": [
            {
                "type": 3,  # STRING
                "name": "message",
                "description": "The message to echo back",
                "required": True
            }
        ]
    },
    {
        "name": "join",
        "description": "Joins your voice channel.",
        "type": 1,  # CHAT_INPUT
    },
    {
        "name": "leave",
        "description": "Leaves the voice channel.",
        "type": 1,  # CHAT_INPUT
    }
]

headers = {"Authorization": f"Bot {TOKEN}"}

r = httpx.put(url, json=commands, headers=headers, timeout=30)
print(f"Commands : {r.status_code}, {r.text}")