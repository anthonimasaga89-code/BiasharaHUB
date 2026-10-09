from app.integrations.social.meta.client import graph_get, graph_post


async def get_instagram_business_account(access_token: str, page_id: str) -> dict:
    return await graph_get(page_id, access_token, {"fields": "instagram_business_account"})


async def create_instagram_container(access_token: str, instagram_id: str, image_url: str, caption: str) -> dict:
    return await graph_post(f"{instagram_id}/media", access_token, {"image_url": image_url, "caption": caption})


async def publish_instagram_container(access_token: str, instagram_id: str, creation_id: str) -> dict:
    return await graph_post(f"{instagram_id}/media_publish", access_token, {"creation_id": creation_id})
