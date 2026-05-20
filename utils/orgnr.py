"""
Validering av norske organisasjonsnummer.

Org.nr er 9 siffer der siste siffer er kontrollsiffer (modulus 11).
Brreg tillater også søk uten kontrollsiffer-validering, men vi validerer
for å fange brukerfeil tidlig.
"""

from __future__ import annotations

import re

# Vekter for de 8 første sifrene (standard mod11 for org.nr)
_MOD11_WEIGHTS = (3, 2, 7, 6, 5, 4, 3, 2)


def normalize_orgnr(raw: str) -> str:
    """Fjern mellomrom og bindestrek, returner kun siffer."""
    return re.sub(r"\D", "", raw.strip())


def is_valid_orgnr(raw: str) -> bool:
    """
    Sjekk om strengen er et gyldig norsk org.nr.

    Eksempel: 984661185 (Posten Bring AS) → True
    """
    orgnr = normalize_orgnr(raw)

    if len(orgnr) != 9 or not orgnr.isdigit():
        return False

    digits = [int(d) for d in orgnr]
    remainder = sum(d * w for d, w in zip(digits[:8], _MOD11_WEIGHTS)) % 11

    if remainder == 0:
        expected_check = 0
    else:
        expected_check = 11 - remainder

    # Kontrollsiffer 10 er ugyldig i org.nr
    if expected_check == 10:
        return False

    return digits[8] == expected_check
