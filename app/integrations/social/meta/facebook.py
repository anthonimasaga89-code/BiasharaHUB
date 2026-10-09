from app.integrations.social.meta.client import graph_post


async def create_page_feed_post(access_token: str, page_id: str, message: str, link: str | None = None) -> dict:
    payload = {"message": message}
    if link:
        payload["link"] = link
    return await graph_post(f"{page_id}/feed", access_token, payload)
