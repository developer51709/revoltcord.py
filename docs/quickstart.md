# Quickstart Guide

This guide shows how to create your first Revolt bot using revoltcord.py.

---

## 🧰 Basic Bot Example

```python
from revoltcord import commands

bot = commands.Bot(command_prefix="!")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")
    
bot.run("YOUR_REVOLT_BOT_TOKEN")
```

---

## 🔑 Getting a Bot Token
1. Log into your Revolt server

2. Go to **Settings → Bots**

3. Click **Create Bot**

4. Copy the generated token

5. Paste it into `bot.run("TOKEN")`

---

## ▶️ Running the Bot
```Code
python bot.py
```

Your bot will connect to the Revolt gateway and begin listening for events.

## 🎉 Next Steps
Explore the API reference

Learn how Discord.py features map to Revolt

Check out more examples in the examples section
