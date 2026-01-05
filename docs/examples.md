# Examples

This page contains example bots demonstrating how to use revoltcord.py.  
As the library grows, more examples will be added.

---

# Basic Ping Bot

```python
from revoltcord import commands

bot = commands.Bot(command_prefix="!")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

bot.run("YOUR_REVOLT_BOT_TOKEN")
```

---

# Echo Bot

```python
from revoltcord import commands

bot = commands.Bot(command_prefix="!")

@bot.command()
async def echo(ctx, *, text: str):
    await ctx.send(text)

bot.run("YOUR_REVOLT_BOT_TOKEN")
```

---

# On‑Message Event Example

```python
from revoltcord import Client

client = Client()

@client.event
async def on_message(message):
    if message.content == "hello":
        await message.channel.send("Hello there!")

client.run("TOKEN")
```

---

# Porting a Discord.py Bot

Here’s an example of a Discord.py  bot that should work with minimal changes:

```python
from revoltcord import commands

bot = commands.Bot(command_prefix="?")

@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(f"The sum is {a + b}")

bot.run("TOKEN")
```

---

# More Examples Coming Soon

Planned examples include:

- Moderation bot

- Reaction roles

- Welcome messages

- Logging system

- Cog‑based bot structure

- API integration bot

Contributions are welcome!
