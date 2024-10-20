import os
import requests
from typing import List, Optional

async def get_mindforge_session_token(
    npc_ids: List[str],
    base_url: str = "https://api.mindforge.ai",
    api_key: Optional[str] = None,
    conversation_id: Optional[str] = None,
    user_id: Optional[str] = None
) -> str:
    """
    Get a Mindforge session token.

    Args:
        npc_ids (List[str]): List of NPC IDs.
        base_url (str, optional): Base URL for the Mindforge API. Defaults to "https://api.mindforge.ai".
        api_key (Optional[str], optional): Mindforge API key. Defaults to None.
        conversation_id (Optional[str], optional): Conversation ID. Defaults to None.
        user_id (Optional[str], optional): User ID. Defaults to None.

    Raises:
        ValueError: If API key is not provided or found in environment variables.
        requests.RequestException: If there's an HTTP error.

    Returns:
        str: The session token.
    """
    mindforge_api_key = api_key or os.environ.get('MINDFORGE_API_KEY')

    if not mindforge_api_key:
        raise ValueError(
            "API key is required. Set MINDFORGE_API_KEY environment variable or pass api_key parameter."
        )

    response = requests.post(
        f"{base_url}/sessions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {mindforge_api_key}"
        },
        json={
            "npcIds": npc_ids,
            "conversationId": conversation_id,
            "userId": user_id
        }
    )

    response.raise_for_status()  # This will raise an HTTPError for bad responses

    data = response.json()
    return data['token']