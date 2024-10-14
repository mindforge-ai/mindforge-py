# Mindforge Client

[mindforge.ai](https://mindforge.ai)

This is a Python client for interacting with the Mindforge API. It provides a simple interface to connect to the Mindforge server, send messages, and receive various types of events.

## Installation

To install the Mindforge client, use pip:

```bash
pip install mindforge
```

## Usage

Create a MindforgeClient:

```python
from mindforge import MindforgeClient, MindforgeServerEventType

api_key = "your-api-key"
client = MindforgeClient(api_key)
```

To use this client, you'll need a Mindforge API key. You can create keys in the dashboard.

### Open a websocket connection

To connect to the Mindforge server:

```python
character_id = "your-character-id"
conversation_id = "optional-conversation-id"
client.connect(character_id, conversation_id)
```

### Sending messages and audio data

To send a text message to the server:

```python
client.send_message("Hello, Mindforge!")
```

To send audio data to the server:

```python
client.send_audio_data("base64-encoded-audio-data")
```

### Receiving data

You can listen for various events emitted by the client:

```python
def on_npc_message(content):
  print("Received NPC message:", content)

def on_npc_action(content):
  print("Received NPC action:", content)

def on_npc_live_message_chunk(content):
  print("Received NPC live message chunk:", content)

def on_npc_live_message(content):
  print("Received complete NPC live message:", content)

def on_npc_audio_data(content):
  print("Received NPC audio data:", content)

def on_player_transcribed_message_chunk(content):
  print("Received player transcribed message chunk:", content)

def on_player_transcribed_message(content):
  print("Received complete player transcribed message:", content)

def on_server_error(content):
  print("Server error:", content)

def on_close():
  print("Connection closed")

client.on(MindforgeServerEventType.NPCMessage, on_npc_message)
client.on(MindforgeServerEventType.NPCAction, on_npc_action)
client.on(MindforgeServerEventType.NPCLiveMessageChunk, on_npc_live_message_chunk)
client.on(MindforgeServerEventType.NPCLiveMessage, on_npc_live_message)
client.on(MindforgeServerEventType.NPCAudioData, on_npc_audio_data)
client.on(MindforgeServerEventType.PlayerTranscribedMessageChunk, on_player_transcribed_message_chunk)
client.on(MindforgeServerEventType.PlayerTranscribedMessage, on_player_transcribed_message)
client.on(MindforgeServerEventType.ServerError, on_server_error)
client.on(MindforgeServerEventType.Close, on_close)
```

### Disconnecting

To disconnect from the server:

```python
client.disconnect()
```

## Event Types

The client uses the following event types:

### Server Event Types

`NPCMessage`: Received when the NPC sends a complete message.

`NPCAction`: Received when the NPC performs an action.

`NPCLiveMessageChunk`: Received when a chunk of the NPC's live message is available.

`NPCLiveMessage`: Received when the NPC's complete live message is available.

`NPCAudioData`: Received when audio data from the NPC is available.

`PlayerTranscribedMessageChunk`: Received when a chunk of the player's transcribed message is available.

`PlayerTranscribedMessage`: Received when the player's complete transcribed message is available.

`ServerError`: Received when an error occurs on the server.

`Close`: Received when the WebSocket connection is closed.

### Client Event Types

`PlayerMessage`: Used to send a text message from the player to the server.

`PlayerAudioData`: Used to send audio data from the player to the server.

## Support

If you need any help or have any questions, please open a GitHub issue or contact us at `team@mindforge.ai`.
