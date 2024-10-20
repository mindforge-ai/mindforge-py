from enum import Enum
from typing import Union, Dict, Any

class MindforgeNPCMessageType(Enum):
    Text = "npc.text"
    InputAudioTranscript = "npc.input_audio_transcript"
    OutputAudioTranscript = "npc.output_audio_transcript"
    ClientFunctionFire = "npc.client_function_fire"

class MindforgeClientMessageType(Enum):
    ClientFunctionResult = "client.function_result"

class MindforgeServerMessageType(Enum):
    ServerFunctionResult = "server.function_result"

class MindforgePlayerMessageType(Enum):
    Text = "player.text"
    TriggerNPCMessage = "player.trigger_npc_message"

class NPCFunctionMessage:
    def __init__(self, name: str, args: Dict[str, Any]):
        self.type = MindforgeNPCMessageType.ClientFunctionFire
        self.name = name
        self.args = args

class NPCContentMessage:
    def __init__(self, type: MindforgeNPCMessageType, content: str):
        self.type = type
        self.content = content

NPCMessage = Union[NPCFunctionMessage, NPCContentMessage]

class NPCText(NPCContentMessage):
    def __init__(self, content: str):
        super().__init__(MindforgeNPCMessageType.Text, content)

class NPCInputAudioTranscript(NPCContentMessage):
    def __init__(self, content: str):
        super().__init__(MindforgeNPCMessageType.InputAudioTranscript, content)

class NPCOutputAudioTranscript(NPCContentMessage):
    def __init__(self, content: str):
        super().__init__(MindforgeNPCMessageType.OutputAudioTranscript, content)

class NPCClientFunctionFire(NPCFunctionMessage):
    def __init__(self, name: str, args: Dict[str, Any]):
        super().__init__(name, args)

class PlayerMessage:
    def __init__(self, type: MindforgePlayerMessageType, content: str):
        self.type = type
        self.content = content

class PlayerText(PlayerMessage):
    def __init__(self, content: str):
        super().__init__(MindforgePlayerMessageType.Text, content)

class PlayerTriggerNPCMessage(PlayerMessage):
    def __init__(self, content: str):
        super().__init__(MindforgePlayerMessageType.TriggerNPCMessage, content)

# MindforgeNPCMessageEventMap equivalent
MindforgeNPCMessageEventMap = {
    MindforgeNPCMessageType.Text: NPCText,
    MindforgeNPCMessageType.InputAudioTranscript: NPCInputAudioTranscript,
    MindforgeNPCMessageType.OutputAudioTranscript: NPCOutputAudioTranscript,
    MindforgeNPCMessageType.ClientFunctionFire: NPCClientFunctionFire,
}