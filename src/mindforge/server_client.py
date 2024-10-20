import os
from typing import List, Dict, Any
import requests
from events import Events

from .messages import (
    NPCMessage,
    MindforgeNPCMessageType,
    NPCClientFunctionFire,
    NPCText
)

class MindforgeServerClient(Events):
    def __init__(self, base_url: str = "https://api.mindforge.ai", api_key: str = None):
        super().__init__()
        self.base_url = base_url
        self.api_key = api_key or os.environ.get('MINDFORGE_API_KEY')
        
        if not self.api_key:
            raise ValueError("[Mindforge] API key missing")

        self.perform = self.Perform(self)

    class Perform:
        def __init__(self, client):
            self.client = client

        async def trigger(self, npc_id: str, history: List[Dict[str, str]]) -> List[NPCMessage]:
            try:
                response = requests.post(
                    f"{self.client.base_url}/perform",
                    json={
                        "npcId": npc_id,
                        "history": history
                    },
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.client.api_key}"
                    }
                )
                response.raise_for_status()
                result: List[Dict[str, Any]] = response.json()

                return [
                    self._create_message(message)
                    for message in result
                ]
            except requests.RequestException as error:
                print(f"Error calling perform API: {error}")
                raise ValueError("Failed to perform NPC interaction")

        @staticmethod
        def _create_message(message: Dict[str, Any]) -> NPCMessage:
            if message['type'] == MindforgeNPCMessageType.Text.value:
                return NPCText(message['content'])
            elif message['type'] == MindforgeNPCMessageType.ClientFunctionFire.value:
                return NPCClientFunctionFire(message['name'], message['args'])
            else:
                raise ValueError("Unknown message type")