# `mindforge-py`

[mindforge.ai](https://mindforge.ai)

This package contains Python clients and utilities for interacting with the Mindforge API. Specifically, there's a `MindforgeServerClient` for interactions with our REST API (e.g. creating an NPC, deleting a capability), and a `MindforgeBrowserClient` for joining live sessions in your client-side code.

## Installation

To install the Mindforge client, use pip:

```bash
pip install mindforge
```

## Server-side Usage

Create a `MindforgeServerClient`:

```python
from mindforge import MindforgeServerClient

client = MindforgeServerClient(
  base_url="https://api.mindforge.ai", # Optional
  api_key="your-api-key"
)
```

To use this client, you'll need a Mindforge API key. You can create keys in the dashboard.

### Performing NPC interactions

To trigger an NPC interaction:

```python
from mindforge.messages import NPCText, NPCClientFunctionFire

npc_id = "your-npc-id" # get from dashboard
history = [
  {"role": "player", "content": "Hello, NPC!"},
  {"role": "npc", "content": "Greetings! How can I assist you today?"},
]

try:
  result = await client.perform.trigger(npc_id, history)
  for message in result:
    if isinstance(message, NPCText):
      print("NPC Text:", message.content)
    elif isinstance(message, NPCClientFunctionFire):
      print("NPC Function:", message.name, message.args)
except ValueError as error:
  print("Error performing NPC interaction:", error)
```

## Browser-side Usage

Create a `MindforgeBrowserClient`:

```python
from mindforge import MindforgeBrowserClient, MindforgeNPCMessageType

client = MindforgeBrowserClient()
```

### Joining a session

To join a live session:

```python
token = "your-session-token" # `get_mindforge_session_token from token.py`

try:
  await client.join_session(token)
  print("Joined session successfully")
except ValueError as error:
  print("Error joining session:", error)
```

### Receiving messages

You can listen for various events emitted by the client:

```python
@client.on(MindforgeNPCMessageType.Text)
def handle_text(message):
  print("Received NPC text:", message.content)

@client.on(MindforgeNPCMessageType.InputAudioTranscript)
def handle_input_transcript(message):
  print("Received input audio transcript:", message.content)

@client.on(MindforgeNPCMessageType.OutputAudioTranscript)
def handle_output_transcript(message):
  print("Received output audio transcript:", message.content)

@client.on(MindforgeNPCMessageType.ClientFunctionFire)
def handle_client_function(message):
  print("NPC triggered client function:", message.name, message.args)
```

### Disconnecting

To disconnect from the session:

```python
client.disconnect()
```

## Event Types

The client uses the following event types:

### Server Event Types

| Event Type                 | Description                                             |
| -------------------------- | ------------------------------------------------------- |
| `NPCText`                  | Received when the NPC sends a text message.             |
| `NPCInputAudioTranscript`  | Received when the input audio transcript is available.  |
| `NPCOutputAudioTranscript` | Received when the output audio transcript is available. |
| `NPCClientFunctionFire`    | Received when the NPC triggers a client-side function.  |

### Client Event Types

| Event Type                | Description                                                |
| ------------------------- | ---------------------------------------------------------- |
| `PlayerText`              | Used to send a text message from the player to the server. |
| `PlayerTriggerNPCMessage` | Used to trigger an NPC message from the player.            |

## Support

If you need any help or have any questions, please open a GitHub issue or contact us at `team@mindforge.ai`.
