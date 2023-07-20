# DisCatCore

A lower level Discord API wrapper that functions as the core layer of DisCatPy.

## Examples

### HTTP

```python
import discatcore
import asyncio

http = discatcore.HTTPClient("token")
CHANNEL = 000000000000000000

async def main():
    try:
        await http.create_message(CHANNEL, content="Hello!")
    finally:
        await http.close()

asyncio.run(main())
```

### Gateway

```python
import discatcore
import asyncio
import discord_typings

http = discatcore.HTTPClient("token")
dispatcher = discatcore.Dispatcher()
# Every intent except the GUILD_MEMBERS, GUILD_PRESENCES, and MESSAGE_CONTENT intents
# calculated via https://discord-intents-calculator.vercel.app
intents = 3243773
gateway = discatcore.GatewayClient(http, dispatcher, intents=intents.value)

@dispatcher.new_event("ready").callback
async def ready(event: discord_typings.ReadyData):
    print(event)

async def main():
    url: str | None = None
    while True:
        try:
            await gateway.connect(url)
        except discatcore.GatewayReconnect as e:
            url = e.url

asyncio.run(main())
```

## Philosophy

DisCatCore tries to be as minimal as possible. The basic functions needed to communicate with the API are provided and nothing else.

Along with being minimal, we also believe in type safety. So that's why the things DisCatCore wrapped support types from `discord_typings`.

## Installing

To install DisCatCore, you will have to install directly from the GitHub repo. Install it via this command:

```bash
# Unix/Linux
python3 -m pip install git+https://github.com/discatpy-dev/core.git

# Windows
py -3 -m pip install git+https://github.com/discatpy-dev/core.git
```

DisCatCore currently has not been released to a PyPi package, so stay tuned for that.
