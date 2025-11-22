import json
from typing import List, Tuple

import httpx

from app.core.config import get_settings

settings = get_settings()


class HFClassifierError(Exception):
    pass


class HFClassifierService:
    def __init__(self):
        if not settings.HF_API_TOKEN:
            raise HFClassifierError("HF_API_TOKEN is missing")

        self.headers = {
            "Authorization": f"Bearer {settings.HF_API_TOKEN}",
            "Content-Type": "application/json"
        }

        self.intent_model_url = f"https://api-inference.huggingface.co/models/{settings.HF_CLASSIFIER_MODEL_ID}"
        self.sentiment_model_url = (
            "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
        )

        with open("app/prompts/classification_labels.json", "r", encoding="utf-8") as f:
            self.labels = json.load(f)

    async def zero_shot_classify(self, text: str, labels: List[str]) -> Tuple[str, float]:
        payload = {
            "inputs": text,
            "parameters": {"candidate_labels": labels}
        }

        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post(self.intent_model_url, headers=self.headers, json=payload)

        if response.status_code >= 400:
            raise HFClassifierError(f"HF Zero-shot classifier error: {response.text}")

        data = response.json()
        best = max(zip(data["scores"], data["labels"]))
        score, label = best
        return label, float(score)

    async def classify_intent(self, text: str) -> Tuple[str, float]:
        return await self.zero_shot_classify(text, self.labels["intents"])

    async def classify_tags(self, text: str) -> Tuple[str, float]:
        return await self.zero_shot_classify(text, self.labels["tags"])

    async def classify_sentiment(self, text: str) -> str:
        payload = {"inputs": text}

        async with httpx.AsyncClient(timeout=45) as client:
            resp = await client.post(self.sentiment_model_url, headers=self.headers, json=payload)

        if resp.status_code >= 400:
            raise HFClassifierError(f"HF Sentiment Error: {resp.text}")

        result = resp.json()
        sentiment = result[0]["label"]  # POSITIVE / NEGATIVE / NEUTRAL
        return sentiment.lower()
