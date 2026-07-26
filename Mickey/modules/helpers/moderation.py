import aiohttp

from config import GROQ_API_KEY

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "meta-llama/llama-guard-4-12b"


async def is_toxic(text: str) -> bool:
    if not text or not GROQ_API_KEY:
        return False

    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": text}],
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                GROQ_URL,
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=5),
            ) as resp:
                data = await resp.json()
        result = data["choices"][0]["message"]["content"].strip().lower()
        return result.startswith("unsafe")
    except Exception:
        return False
        
