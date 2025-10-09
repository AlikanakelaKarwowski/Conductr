# gateway/main.py
import os
import sys
import signal
import asyncio
import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN_ENV = "DISCORD_BOT_TOKEN"

intents = discord.Intents.none()
intents.guilds = True
intents.voice_states = True

shutdown_event = asyncio.Event()


def _handle_signal(*_):
    print("gateway: received shutdown signal", flush=True)
    shutdown_event.set()


async def runner(client: discord.AutoShardedClient):
    # wait until fully logged in
    await client.wait_until_ready()
    print(f"gateway: logged in as {client.user} (id={client.user.id})", flush=True)
    print(f"gateway: shard_count={client.shard_count}", flush=True)
    await shutdown_event.wait()
    await client.close()


class Bot(discord.AutoShardedClient):
    async def on_ready(self):
        # fires when first shard is ready
        print("gateway: on_ready()", flush=True)


def main():
    token = os.getenv(TOKEN_ENV)
    if not token:
        print(
            f"ERROR: set {TOKEN_ENV} in your environment.", file=sys.stderr, flush=True
        )
        sys.exit(1)

    shard_count = int(os.getenv("TOTAL_SHARDS", "1"))
    print(f"gateway: starting with TOTAL_SHARDS={shard_count}", flush=True)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, _handle_signal)
        except NotImplementedError:
            pass

    client = Bot(intents=intents, shard_count=shard_count)

    async def start():
        # start runner AFTER we’ve created the proper client instance
        loop.create_task(runner(client))
        await client.start(token, reconnect=True)

    try:
        loop.run_until_complete(start())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        print("gateway: shutdown complete.", flush=True)


if __name__ == "__main__":
    main()
