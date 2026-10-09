import httpx
from app.core.config import settings


async def send_text_message(access_token: str, phone_number_id: str, recipient: str, body: str) -> dict:
    url = f"https://graph.facebook.com/{settings.META_GRAPH_VERSION}/{phone_number_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "text",
        "text": {"body": body},
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(url, headers={"Authorization": f"Bearer {access_token}"}, json=payload)
    response.raise_for_status()
    return response.json()
