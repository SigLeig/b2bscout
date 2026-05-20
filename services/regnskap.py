"""
Klient for Brønnøysundregistrenes Regnskapsregister-API.

Dokumentasjon: https://data.brreg.no/regnskapsregisteret/regnskap/swagger-ui/index.html

Endepunkt: GET /regnskap/{orgnr}
Returnerer liste med årsregnskap — vi henter nyeste og trekker ut nøkkeltall.
"""

from __future__ import annotations

from typing import Any

import requests

from config import settings


class RegnskapError(Exception):
    """Feil ved henting av regnskap."""


class RegnskapNotFoundError(RegnskapError):
    """Ingen regnskap funnet for org.nr."""


def fetch_regnskap_raw(orgnr: str, timeout: int = 15) -> list[dict[str, Any]]:
    """Hent rå JSON-liste med regnskap for gitt org.nr."""
    url = f"{settings.regnskap_base_url}/{orgnr}"
    response = requests.get(
        url,
        headers={"Accept": "application/json"},
        timeout=timeout,
    )

    if response.status_code == 404:
        raise RegnskapNotFoundError(f"Ingen regnskap for org.nr {orgnr}")
    if not response.ok:
        raise RegnskapError(
            f"Regnskapsregisteret returnerte HTTP {response.status_code}: {response.text[:200]}"
        )

    data = response.json()
    if not isinstance(data, list):
        raise RegnskapError("Uventet responsformat fra Regnskapsregisteret")
    return data


def parse_latest_regnskap(raw_list: list[dict[str, Any]]) -> dict[str, Any] | None:
    """
    Trekk ut salgsrelevante nøkkeltall fra nyeste regnskap.

    JSON-struktur (forenklet):
      resultatregnskapResultat
        └── driftsresultat
              ├── driftsinntekter.sumDriftsinntekter  → omsetning
              └── driftsresultat                      → driftsresultat
        └── aarsresultat
      egenkapitalGjeld
        ├── egenkapital.sumEgenkapital
        └── gjeldOversikt.sumGjeld
      eiendeler.sumEiendeler
    """
    if not raw_list:
        return None

    sorted_items = sorted(
        raw_list,
        key=lambda item: item.get("regnskapsperiode", {}).get("tilDato", ""),
        reverse=True,
    )
    latest = sorted_items[0]
    periode = latest.get("regnskapsperiode", {})
    drifts = latest.get("resultatregnskapResultat", {}).get("driftsresultat", {})
    resultat = latest.get("resultatregnskapResultat", {})
    egenkapital_gjeld = latest.get("egenkapitalGjeld", {})

    return {
        "regnskapsaar": periode.get("tilDato", "")[:4],
        "periode_fra": periode.get("fraDato"),
        "periode_til": periode.get("tilDato"),
        "valuta": latest.get("valuta", "NOK"),
        "omsetning_nok": drifts.get("driftsinntekter", {}).get("sumDriftsinntekter"),
        "driftsresultat_nok": drifts.get("driftsresultat"),
        "aarsresultat_nok": resultat.get("aarsresultat"),
        "sum_eiendeler_nok": latest.get("eiendeler", {}).get("sumEiendeler"),
        "egenkapital_nok": egenkapital_gjeld.get("egenkapital", {}).get("sumEgenkapital"),
        "sum_gjeld_nok": egenkapital_gjeld.get("gjeldOversikt", {}).get("sumGjeld"),
    }


def fetch_regnskap_summary(orgnr: str) -> dict[str, Any] | None:
    """Hent og parse nyeste regnskap. Returnerer None hvis ikke funnet."""
    try:
        raw = fetch_regnskap_raw(orgnr)
        return parse_latest_regnskap(raw)
    except RegnskapNotFoundError:
        return None
