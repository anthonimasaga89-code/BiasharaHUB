import httpx
from app.core.config import settings


async def generate_text(prompt: str) -> str:
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured")
    payload = {
        "model": settings.OPENAI_MODEL,
        "input": prompt,
    }
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            "https://api.openai.com/v1/responses",
            headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
            json=payload,
        )
    response.raise_for_status()
    data = response.json()
    if data.get("output_text"):
        return data["output_text"]
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                return content.get("text", "")
    return ""
