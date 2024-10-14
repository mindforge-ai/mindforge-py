from events import Events
from enum import Enum
from typing import Optional
import json
import websocket
from .messages import MindforgeServerEventType, PlayerMessage, PlayerAudioData, send_websocket_message

class MindforgeClient:
    def __init__(self, api_key: str, base_url: str = "https://api.mindforge.ai"):
        self.api_key = api_key
        self.base_url = base_url
        self.ws = None
        self.events = Events()

    def connect(self, character_id: str, conversation_id: Optional[str] = None):
        url = f"{self.base_url}/characters/{character_id}/perform/stream?token={self.api_key}"
        if conversation_id:
            url += f"&_conversation_id={conversation_id}"
        
        self.ws = websocket.WebSocketApp(
            url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close
        )
        self.ws.run_forever()

    def _on_open(self, ws):
        print("Connected to Mindforge server")

    def _on_message(self, ws, message):
        try:
            server_event = json.loads(message)
            event_type = MindforgeServerEventType(server_event["type"])
            self.events.emit(event_type.value, server_event.get("content"))
        except json.JSONDecodeError:
            self.events.emit(MindforgeServerEventType.ServerError.value, "Failed to parse server event")

    def _on_error(self, ws, error):
        self.events.emit(MindforgeServerEventType.ServerError.value, "WebSocket error occurred")

    def _on_close(self, ws, close_status_code, close_msg):
        self.events.emit(MindforgeServerEventType.Close.value)

    def send_message(self, message: str):
        if self.ws and self.ws.sock and self.ws.sock.connected:
            send_websocket_message(self.ws, PlayerMessage(message))
        else:
            raise ConnectionError("WebSocket is not connected")

    def send_audio_data(self, audio_data: str):
        if self.ws and self.ws.sock and self.ws.sock.connected:
            send_websocket_message(self.ws, PlayerAudioData(audio_data))
        else:
            raise ConnectionError("WebSocket is not connected")

    def disconnect(self):
        if self.ws:
            self.ws.close()

    def on(self, event_type: MindforgeServerEventType, callback):
        self.events.on(event_type.value, callback)