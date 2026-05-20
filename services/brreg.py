"""
Klient for Brønnøysundregistrenes åpne Enhetsregister-API.

Dokumentasjon: https://data.brreg.no/enhetsregisteret/api/docs/

Endepunkter:
  GET /enheter?navn=...       → søk etter firmanavn
  GET /enheter/{orgnr}       → grunndata om hovedenhet
  GET /enheter/{orgnr}/roller → roller
"""

from __future__ import annotations

from typing import Any

import requests

from config import settings


class BrregError(Exception):
    """Baseklasse for Brreg-relaterte feil."""


class BrregNotFoundError(BrregError):
    """Org.nr finnes ikke i registeret."""


class BrregClient:
    """Enkel HTTP-klient mot Brreg sitt REST-API."""

    def __init__(self, base_url: str | None = None, timeout: int = 15) -> None:
        self.base_url = (base_url or settings.brreg_base_url).rstrip("/")
        self.timeout = timeout

    def search_enheter_by_navn(
        self, navn_fragment: str, size: int = 15
    ) -> list[dict[str, Any]]:
        """
        Søk etter enheter med navnet som DELSTRENG (Brreg fulltekstsøk).

        Returnerer tom liste ved 0 treff eller tom query.
        """
        q = (navn_fragment or "").strip()
        if len(q) < 2:
            return []

        url = f"{self.base_url}/enheter"
        response = requests.get(
            url,
            params={"navn": q, "size": min(size, 50)},
            headers={"Accept": "application/json"},
            timeout=self.timeout,
        )
        if not response.ok:
            raise BrregError(
                f"Brreg søk returnerte HTTP {response.status_code}: {response.text[:200]}"
            )
        data = response.json()
        embedded = data.get("_embedded") or {}
        return embedded.get("enheter") or []

    def _get(self, path: str) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        response = requests.get(
            url,
            headers={"Accept": "application/json"},
            timeout=self.timeout,
        )

        if response.status_code == 404:
            raise BrregNotFoundError(f"Ingen enhet funnet for {path}")
        if not response.ok:
            raise BrregError(
                f"Brreg returnerte HTTP {response.status_code}: {response.text[:200]}"
            )

        return response.json()

    def fetch_enhet(self, orgnr: str) -> dict[str, Any]:
        """
        Hent hovedenhet (selskap) for gitt org.nr.

        Responsen er et flatt JSON-objekt med selskapsdata.
        Se utils/formatters.py for hvordan feltene tolkes.
        """
        return self._get(f"/enheter/{orgnr}")

    def fetch_roller(self, orgnr: str) -> dict[str, Any]:
        """
        Hent roller knyttet til enheten.

        Responsen er et objekt med nøkkelen 'rollegrupper', som er en liste
        av grupper (Styre, Daglig leder, Revisor, ...). Hver gruppe inneholder
        en liste 'roller' med personer eller enheter.
        """
        return self._get(f"/enheter/{orgnr}/roller")

    def fetch_company_bundle(self, orgnr: str) -> tuple[dict[str, Any], dict[str, Any]]:
        """Hent både enhetsdata og roller i én operasjon."""
        enhet = self.fetch_enhet(orgnr)
        roller = self.fetch_roller(orgnr)
        return enhet, roller
