"""
Sentral konfigurasjon for B2B Scout.

Leser innstillinger fra miljøvariabler (eller .env-fil via python-dotenv).
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Alle konfigurerbare verdier samlet på ett sted."""

    provider: str = os.getenv("PROVIDER", "groq").lower()
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    xai_api_key: str = os.getenv("XAI_API_KEY", "")
    xai_model: str = os.getenv("XAI_MODEL", "grok-4.3")
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    openrouter_model: str = os.getenv(
        "OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct"
    )
    news_api_key: str = os.getenv("NEWS_API_KEY", "")
    brreg_base_url: str = "https://data.brreg.no/enhetsregisteret/api"
    regnskap_base_url: str = "https://data.brreg.no/regnskapsregisteret/regnskap"


settings = Settings()
