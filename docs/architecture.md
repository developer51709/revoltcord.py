# Architecture Overview

This document explains the internal architecture of **revoltcord.py** and how its components work together to emulate the Discord.py API on top of the Revolt platform.

---

# High‑Level Design

revoltcord.py is built around three core layers:

1. **Gateway Layer**  
   Handles WebSocket communication with the Revolt gateway.

2. **REST Layer**  
   Wraps Revolt’s REST API with Pythonic methods.

3. **Compatibility Layer**  
   Recreates Discord.py’s public API (commands, events, models).

These layers work together to translate Discord.py‑style bot code into Revolt API calls.

---

# Layer Breakdown

## 1. Gateway Layer (`gateway.py`)

Responsibilities:
- Connect to the Revolt WebSocket gateway
- Receive real‑time events (messages, joins, updates)
- Normalize event payloads
- Dispatch events to the Bot object

This layer acts as the “event engine” of the library.

---

## 2. REST Layer (`http.py`)

Responsibilities:
- Send HTTP requests to Revolt’s REST API
- Handle authentication via bot token
- Provide helper methods such as:
  - `send_message()`
  - `edit_message()`
  - `delete_message()`
  - `fetch_user()`
  - `fetch_channel()`

This layer ensures all network operations are cleanly abstracted.

---

## 3. Compatibility Layer (`commands.py`, `client.py`, `models/`)

This is the heart of the project.

Responsibilities:
- Provide Discord.py‑style classes (`Bot`, `Context`, `Message`, etc.)
- Implement decorators like `@bot.command()`
- Dispatch events to user‑defined handlers
- Wrap Revolt objects in Discord‑like models

This layer ensures that existing Discord.py bot code can run with minimal or no changes.

---

# Event Flow

1. Revolt sends a WebSocket event  
2. `gateway.py` receives it  
3. The event is normalized  
4. The Bot’s `dispatch()` method is called  
5. User‑defined event handlers run  
6. Commands are parsed and executed  
7. Responses are sent via the REST layer

---

# Command Flow

1. User sends a message  
2. Gateway receives the message event  
3. Bot checks if the message starts with the command prefix  
4. If so, the command is matched  
5. A `Context` object is created  
6. The command function is executed  
7. Output is sent back to Revolt

---

# Future Architecture Plans

- Cog system for modular bot design  
- Extension loader  
- Slash command emulation  
- Thread support  
- Voice event support (if Revolt expands its API)

---

# Summary

The architecture is intentionally modular and familiar to Discord.py developers.  
Each layer is isolated, making the library easy to maintain, extend, and contribute to.
