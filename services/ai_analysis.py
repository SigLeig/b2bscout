"""
AI-analyse via Groq, xAI (Grok) eller OpenRouter.
"""

from __future__ import annotations

import requests

from config import settings

SYSTEM_PROMPT = """
Du er en erfaren B2B-salgstrateg i det norske markedet.

Du får input i user-meldingen:
  0. Selgerens selskap (valgfritt, ofte hovedkontekst) — hvem som selger
  1. Selgerens produkt/tjeneste (valgfritt tillegg) — hva som skal selges inn
  2. Kundens Brreg-data
  3. Kundens regnskapstall
  4. Dagsaktuelle nyheter om kunden

Selgerens selskap og produkt kan brukes hver for seg eller sammen.
Hvis bare selskap er oppgitt: posisjonér ut fra «Hva selgerens firma driver med» og bransje i prompten.
Hvis bare produkt er oppgitt: posisjonér ut fra produktet.
Hvis begge: kombiner dem.
Når selgerens selskap-seksjon inneholder navn og virksomhetsbeskrivelse, skal du bruke den — ikke hevde at data mangler.

VIKTIG REKKEFØLGE I ANALYSEN:
  Først vurder kundens økonomiske helse (regnskap + Brreg-risiko).
  Deretter produktmatch mot selgerens selskap/produkt.
  Til slutt konkret pitch og mulige ekstra muligheter.

Lag salgsanalyse på norsk med disse seksjonene:

1. **Selskapsprofil** – hvem er de, størrelse, bransje, modenhet
2. **Økonomisk helse** – omsetning, driftsresultat, egenkapital/gjeld, konkursflagg.
   Konkluder eksplisitt: Har selskapet råd til en investering nå? (Ja/Nei/Dusiv + begrunnelse)
3. **Produktmatch** – hvorfor selgerens tilbud passer (eller ikke passer) kunden.
   Bruk «Hva selgerens firma driver med» fra Brreg når selgerselskap er oppgitt.
   Ikke skriv at selger/produkt mangler når selgerens selskap-seksjon i prompten er fylt ut.
4. **Kjøpssignaler** – kombiner nyheter og Brreg-data, spisset mot selgerens produkt.
   Referer til artikkel-titler og tall der det er mulig.
5. **Anbefalt beslutningstaker** – hvem bør kontaktes først og hvorfor
6. **Samtalevinkler** – 3 icebreakers som naturlig leder mot selgerens produkt
7. **Anbefalt neste steg** – én konkret handling for selgeren denne uken

Vær presis, unngå generiske råd, og marker tydelig når du spekulerer utover dataene.
""".strip()


class AIAnalysisError(Exception):
    """Feil ved kall til AI-leverandør."""


def _call_groq(user_prompt: str) -> str:
    if not settings.groq_api_key:
        raise AIAnalysisError("GROQ_API_KEY mangler. Legg den i .env-filen.")

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.groq_api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": settings.groq_model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.4,
        },
        timeout=90,
    )

    if not response.ok:
        raise AIAnalysisError(f"Groq-feil ({response.status_code}): {response.text[:300]}")

    data = response.json()
    return data["choices"][0]["message"]["content"]


def _call_xai(user_prompt: str) -> str:
    if not settings.xai_api_key:
        raise AIAnalysisError("XAI_API_KEY mangler. Legg den i .env-filen.")

    response = requests.post(
        "https://api.x.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.xai_api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": settings.xai_model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.4,
        },
        timeout=90,
    )

    if not response.ok:
        raise AIAnalysisError(f"Grok/xAI-feil ({response.status_code}): {response.text[:300]}")

    data = response.json()
    return data["choices"][0]["message"]["content"]


def _call_openrouter(user_prompt: str) -> str:
    if not settings.openrouter_api_key:
        raise AIAnalysisError("OPENROUTER_API_KEY mangler. Legg den i .env-filen.")

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://b2b-scout.local",
            "X-Title": "B2B Scout",
        },
        json={
            "model": settings.openrouter_model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.4,
        },
        timeout=90,
    )

    if not response.ok:
        raise AIAnalysisError(
            f"OpenRouter-feil ({response.status_code}): {response.text[:300]}"
        )

    data = response.json()
    return data["choices"][0]["message"]["content"]


def generate_sales_analysis(company_prompt: str, provider: str | None = None) -> str:
    """Send selskapsdata til valgt AI-leverandør og returner analysen."""
    provider = (provider or settings.provider).lower()

    if provider == "groq":
        return _call_groq(company_prompt)
    if provider in ("grok", "xai"):
        return _call_xai(company_prompt)
    if provider == "openrouter":
        return _call_openrouter(company_prompt)

    raise AIAnalysisError(
        f"Ukjent PROVIDER: {provider}. Bruk 'groq', 'grok' eller 'openrouter'."
    )
