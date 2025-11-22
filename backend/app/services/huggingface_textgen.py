import httpx
from app.core.config import get_settings

settings = get_settings()


class HFTextGenError(Exception):
    pass


class HFTextGenService:
    def __init__(self):
        if not settings.HF_API_TOKEN:
            raise HFTextGenError("HF_API_TOKEN is missing")
        self.headers = {
            "Authorization": f"Bearer {settings.HF_API_TOKEN}",
            "Content-Type": "application/json"
        }
        self.url = f"https://api-inference.huggingface.co/models/{settings.HF_TEXTGEN_MODEL_ID}"

    async def generate(
        self,
        prompt: str,
        max_new_tokens: int = 250,
        temperature: float = 0.3,
    ) -> str:
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_new_tokens,
                "temperature": temperature,
                "return_full_text": False,
            },
        }

        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(self.url, headers=self.headers, json=payload)

        if resp.status_code == 429:
            raise HFTextGenError("Rate limited by HuggingFace API (429).")
        if resp.status_code >= 400:
            raise HFTextGenError(f"HuggingFace TextGen Error {resp.status_code}: {resp.text}")

        data = resp.json()
        if isinstance(data, list) and data and "generated_text" in data[0]:
            return data[0]["generated_text"].strip()

        raise HFTextGenError("Unexpected HF text generation format")
