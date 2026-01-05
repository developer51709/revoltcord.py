# API Reference

This section documents the public interfaces of **revoltcord.py**.  
Because the library is in early development, this reference will expand as features are implemented.

---

# Client

## `class revoltcord.Client()`
The base client used to connect to the Revolt gateway and REST API.

### Methods

#### `run(token: str)`
Connects the bot to the Revolt gateway using the provided bot token.

#### `close()`
Closes the WebSocket connection and shuts down the client.

---

# Bot

## `class revoltcord.commands.Bot(command_prefix: str)`
A Discord.py‑style bot class that provides command handling and event dispatch.

### Parameters
- `command_prefix`: The prefix used to invoke commands (e.g., `"!"`).

### Methods

#### `command(name: Optional[str] = None)`
Decorator used to register a command.

#### `add_command(command)`
Registers a command object manually.

#### `dispatch(event_name: str, *args)`
Internal method used to dispatch events to listeners.

#### `run(token: str)`
Starts the bot and connects to the Revolt gateway.

---

# Context

## `class revoltcord.commands.Context`
Represents the context of a command invocation.

### Attributes
- `message`: The message that triggered the command.
- `author`: The user who invoked the command.
- `channel`: The channel where the command was used.
- `server`: The server (if any) where the command was used.

### Methods

#### `send(content: str)`
Sends a message to the context’s channel.

---

# Models

## `class revoltcord.Message`
Represents a message sent in a channel.

### Attributes
- `id`
- `content`
- `author`
- `channel`

### Methods

#### `edit(content: str)`
Edits the message.

#### `delete()`
Deletes the message.

---

## `class revoltcord.User`
Represents a Revolt user.

### Attributes
- `id`
- `username`
- `avatar`

---

## `class revoltcord.Channel`
Represents a channel in a server or DM.

### Methods

#### `send(content: str)`
Sends a message to the channel.

---

# Events

The following events are planned:

- `on_ready()`
- `on_message(message)`
- `on_member_join(user)`
- `on_member_leave(user)`
- `on_error(event, *args)`

More events will be added as Revolt’s gateway features expand.

---

# Notes

This API reference will grow significantly as the library matures.  
For now, it serves as a foundation for early contributors.
