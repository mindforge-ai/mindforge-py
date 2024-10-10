import json
import websocket
from enum import Enum
from typing import Optional
from urllib.parse import urlencode
import threading

class MindforgeServerEvent(Enum):
    AUDIO_DATA = "audioData"
    TEXT_DATA = "textData"
    ERROR = "error"
    CLOSE = "close"

class MindforgeClient:
    def __init__(self, api_key: str, base_url: str = "https://api.mindforge.ai"):
        self.api_key = api_key
        self.base_url = base_url
        self.ws: Optional[websocket.WebSocketApp] = None
        self.listeners = {event: [] for event in MindforgeServerEvent}
        self.ws_thread: Optional[threading.Thread] = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self, character_id: str, conversation_id: Optional[str] = None):
        params = {
            "token": self.api_key
        }
        if conversation_id:
            params["_conversation_id"] = conversation_id

        url = f"{self.base_url}/characters/{character_id}/perform/stream?{urlencode(params)}"
        
        self.ws = websocket.WebSocketApp(
            url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close
        )
        self.ws_thread = threading.Thread(target=self.ws.run_forever)
        self.ws_thread.start()

    def _on_open(self, ws):
        print("Connected to Mindforge server")

    def _on_message(self, ws, message):
        try:
            parsed_data = json.loads(message)
            if parsed_data["type"] == "audio":
                self._emit(MindforgeServerEvent.AUDIO_DATA, parsed_data["data"])
            elif parsed_data["type"] == "text":
                self._emit(MindforgeServerEvent.TEXT_DATA, parsed_data["data"])
        except json.JSONDecodeError:
            self._emit(MindforgeServerEvent.ERROR, "Failed to parse server message")

    def _on_error(self, ws, error):
        self._emit(MindforgeServerEvent.ERROR, error)

    def _on_close(self, ws, close_status_code, close_msg):
        self._emit(MindforgeServerEvent.CLOSE)

    def send_message(self, message: str):
        if self.ws and self.ws.sock and self.ws.sock.connected:
            self.ws.send(json.dumps({"type": "userMessage", "content": message}))
        else:
            raise Exception("WebSocket is not connected")

    def disconnect(self):
        if self.ws:
            self.ws.close()
        if self.ws_thread:
            self.ws_thread.join()

    def on(self, event: MindforgeServerEvent, callback):
        self.listeners[event].append(callback)

    def _emit(self, event: MindforgeServerEvent, data=None):
        for callback in self.listeners[event]:
            callback(data)