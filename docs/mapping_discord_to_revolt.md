# Discord.py → Revolt Mapping Guide

This guide explains how Discord concepts translate to Revolt, helping you migrate bots with minimal changes.

---

## 🧩 Concept Mapping

| Discord.py | Revolt | Notes |
|------------|--------|-------|
| Guild | Server | Nearly identical |
| Channel | Channel | Same concept |
| Member | User | Revolt does not distinguish user/member objects |
| Role | Role | Similar permission model |
| Message | Message | Very similar |
| DMChannel | DirectMessage | Same purpose |
| Intents | Not required | Revolt sends all events |

---

## 🛠 API Mapping Examples

### Sending a Message

**Discord.py**
```python
await ctx.send("Hello!")
```

**revoltcord.py**
```python
await ctx.send("Hello!")
```

(Identical — handled by the compatibility layer.)

---

### Editing a Message

**Discord.py**
```python
await message.edit(content="Updated")
```

**revoltcord.py**
```python
await message.edit(content="Updated")
```

---

### Fetching a User

**Discord.py**
```python
user = await bot.fetch_user(id)
```

**revoltcord.py**
```python
user = await bot.fetch_user(id)
```

---

More mappings will be added as the library evolves.
