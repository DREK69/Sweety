import aiohttp

from config import MODERATION_API_KEY, MODERATION_API_URL, PERSPECTIVE_API_KEY

PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


async def _check_perspective(text: str, threshold: float) -> bool:
    payload = {
        "comment": {"text": text},
        "languages": ["en", "hi"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    params = {"key": PERSPECTIVE_API_KEY}
    async with aiohttp.ClientSession() as session:
        async with session.post(
            PERSPECTIVE_URL,
            params=params,
            json=payload,
            timeout=aiohttp.ClientTimeout(total=5),
        ) as resp:
            data = await resp.json()
    return data["attributeScores"]["TOXICITY"]["summaryScore"]["value"] >= threshold


async def _check_generic(text: str, threshold: float) -> bool:
    headers = {"Authorization": f"Bearer {MODERATION_API_KEY}"}
    payload = {"input": text}
    async with aiohttp.ClientSession() as session:
        async with session.post(
            MODERATION_API_URL,
            headers=headers,
            json=payload,
            timeout=aiohttp.ClientTimeout(total=5),
        ) as resp:
            data = await resp.json()
    result = data["results"][0]
    if "flagged" in result:
        return bool(result["flagged"])
    scores = result.get("category_scores", {})
    return any(score >= threshold for score in scores.values())


async def is_toxic(text: str, threshold: float = 0.75) -> bool:
    if not text:
        return False

    try:
        if PERSPECTIVE_API_KEY:
            return await _check_perspective(text, threshold)
        if MODERATION_API_URL and MODERATION_API_KEY:
            return await _check_generic(text, threshold)
    except Exception:
        return False

    return False
