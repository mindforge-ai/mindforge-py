from events import Events
from livekit import Room, RoomEvent, Participant, DataPacket_Kind
from .messages import (
    NPCMessage,
    MindforgeNPCMessageType,
    NPCClientFunctionFire,
    NPCInputAudioTranscript,
    NPCOutputAudioTranscript,
    NPCText,
    PlayerText,
)
import json
from typing import Callable, List, Optional, Any

class MindforgeBrowserClient(Events):
    def __init__(self):
        super().__init__()
        self.room: Optional[Room] = None

    def on(self, event: MindforgeNPCMessageType, listener: Callable[[Any], None]):
        return super().on(event, listener)

    def emit(self, event: MindforgeNPCMessageType, data: Any) -> bool:
        return super().emit(event, data)

    async def join_session(self, token: str) -> None:
        if not token:
            raise ValueError("Token is required")
        
        self.room = Room()
        await self.room.connect("wss://mindforgeai-d4ssqx5a.livekit.cloud", token)
        print("Connected to room", self.room.name)

        await self.room.local_participant.set_microphone_enabled(True)

        self.room.on("participant_connected", lambda participant: 
            print("Participant connected:", participant.identity))

        self.room.on("participant_disconnected", lambda participant: 
            print("Participant disconnected:", participant.identity))

        self.room.on(RoomEvent.DATA_RECEIVED, self._handle_data_received)

    def _handle_data_received(self, payload: bytes, participant: Optional[Participant] = None, kind: Optional[DataPacket_Kind] = None) -> None:
        str_data = payload.decode('utf-8')
        print("Data received from", participant.identity if participant else "unknown", ":", str_data)

        try:
            data: NPCMessage = json.loads(str_data)

            if data['type'] == MindforgeNPCMessageType.Text.value:
                self.emit(MindforgeNPCMessageType.Text, NPCText(data['content']))
            elif data['type'] == MindforgeNPCMessageType.InputAudioTranscript.value:
                self.emit(MindforgeNPCMessageType.InputAudioTranscript, NPCInputAudioTranscript(data['content']))
            elif data['type'] == MindforgeNPCMessageType.OutputAudioTranscript.value:
                self.emit(MindforgeNPCMessageType.OutputAudioTranscript, NPCOutputAudioTranscript(data['content']))
            elif data['type'] == MindforgeNPCMessageType.ClientFunctionFire.value:
                self.emit(MindforgeNPCMessageType.ClientFunctionFire, NPCClientFunctionFire(data['name'], data['args']))
        except json.JSONDecodeError as error:
            print("Error parsing received data:", error)

    def mute_mic(self) -> None:
        if self.room:
            self.room.local_participant.set_microphone_enabled(False)
            print("Microphone muted")
        else:
            raise RuntimeError("Room is not connected")

    def unmute_mic(self) -> None:
        if self.room:
            self.room.local_participant.set_microphone_enabled(True)
            print("Microphone unmuted")
        else:
            raise RuntimeError("Room is not connected")

    def send_text(self, content: str, reliable: bool = True, destination_identities: Optional[List[str]] = None) -> None:
        if self.room:
            player_text = PlayerText(content)
            str_data = json.dumps(player_text.__dict__)
            data = str_data.encode('utf-8')

            self.room.local_participant.publish_data(
                data,
                reliable=reliable,
                destination_identities=destination_identities
            )
            print("Message sent:", content)
        else:
            raise RuntimeError("Room is not connected")

    def disconnect(self) -> None:
        if self.room:
            self.room.disconnect()