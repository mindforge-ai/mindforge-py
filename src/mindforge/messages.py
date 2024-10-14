from enum import Enum
from typing import Optional
import json
import websocket

class MindforgeServerEventType(Enum):
    NPCMessage = "server.npc.message"
    NPCAction = "server.npc.action"
    NPCLiveMessageChunk = "server.npc.live.message_chunk"
    NPCLiveMessage = "server.npc.live.message"
    NPCAudioData = "server.npc.audio_data"
    PlayerTranscribedMessageChunk = "server.player.transcribed_message_chunk"
    PlayerTranscribedMessage = "server.player.transcribed_message"
    ServerError = "server.error"
    Close = "close"

class MindforgeClientEventType(Enum):
    PlayerMessage = "client.player.message"
    PlayerAudioData = "client.player.audio_data"

class MindforgeServerEvent:
    def __init__(self, type: MindforgeServerEventType, content: Optional[str] = None):
        self.type = type
        self.content = content

class MindforgeClientEvent:
    def __init__(self, type: MindforgeClientEventType, content: Optional[str] = None):
        self.type = type
        self.content = content

class NPCMessage(MindforgeServerEvent):
    def __init__(self, content: str):
        super().__init__(MindforgeServerEventType.NPCMessage, content)

class NPCAction(MindforgeServerEvent):
    def __init__(self, content: str):
        super().__init__(MindforgeServerEventType.NPCAction, content)

class NPCLiveMessageChunk(MindforgeServerEvent):
    def __init__(self, content: str):
        super().__init__(MindforgeServerEventType.NPCLiveMessageChunk, content)

class NPCLiveMessage(MindforgeServerEvent):
    def __init__(self, content: str):
        super().__init__(MindforgeServerEventType.NPCLiveMessage, content)

class NPCAudioData(MindforgeServerEvent):
    def __init__(self, content: str):
        super().__init__(MindforgeServerEventType.NPCAudioData, content)

class PlayerTranscribedMessageChunk(MindforgeServerEvent):
    def __init__(self, content: str):
        super().__init__(MindforgeServerEventType.PlayerTranscribedMessageChunk, content)

class PlayerTranscribedMessage(MindforgeServerEvent):
    def __init__(self, content: str):
        super().__init__(MindforgeServerEventType.PlayerTranscribedMessage, content)

class PlayerMessage(MindforgeClientEvent):
    def __init__(self, content: str):
        super().__init__(MindforgeClientEventType.PlayerMessage, content)

class PlayerAudioData(MindforgeClientEvent):
    def __init__(self, content: str):
        super().__init__(MindforgeClientEventType.PlayerAudioData, content)

class ServerError(MindforgeServerEvent):
    def __init__(self, content: str):
        super().__init__(MindforgeServerEventType.ServerError, content)

class Close(MindforgeServerEvent):
    def __init__(self):
        super().__init__(MindforgeServerEventType.Close)

def send_websocket_message(ws: websocket.WebSocket, event: MindforgeClientEvent):
    payload = {"type": event.type.value}
    if event.content:
        payload["content"] = event.content
    ws.send(json.dumps(payload))