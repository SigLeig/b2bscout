"""
Firmanavn-søk mot Brreg med forslag mens brukeren skriver.

Streamlit re-renderer kun fragmentet ved endring av inndata her — mindre hakking
enn full side-rerun ved hvert tastetrykk.

Krever Streamlit>=1.33 (`st.fragment`).
"""

from __future__ import annotations

import html
from typing import Any

import streamlit as st

from services.brreg import BrregClient, BrregError
from utils.orgnr import is_valid_orgnr, normalize_orgnr

SESSION_KEY_SELECTED_ORGNR = "orgnr_from_name_search"


def format_company_hit(enhet: dict[str, Any]) -> str:
    """Én linje tekst til selectbox."""
    navn = enhet.get("navn", "Ukjent navn")
    orgnr = enhet.get("organisasjonsnummer", "")
    adr = enhet.get("forretningsadresse") or {}
    sted = (adr.get("kommune") or adr.get("poststed") or "").strip()

    parts = [navn]
    if sted:
        parts.append(sted)
    if orgnr:
        parts.append(orgnr)
    return " · ".join(parts)


def _fragment_decorator():
    if hasattr(st, "fragment"):
        return st.fragment
    raise RuntimeError(
        "Installer nyere Streamlit: pip install -U streamlit  (>=1.33)"
    )


@_fragment_decorator()
def render_company_autocomplete(
    fragment_key_prefix: str,
    *,
    output_session_key: str = SESSION_KEY_SELECTED_ORGNR,
    label: str = "Firmanavn",
    placeholder: str = "F.eks. Hydro Aluminium, Equinor, Posten…",
    hint: str = "",
    success_suffix: str = "Trykk **Analyser** når du er klar.",
    navn_session_key: str | None = None,
) -> None:
    """
    Tekstfelt + nedtrekk med treff fra Brreg.

    `fragment_key_prefix` må være unik per visning (-- landing vs dash).
    """
    key_q = f"firm_navn_query_{fragment_key_prefix}"
    key_sb = f"firm_navn_pick_{fragment_key_prefix}"

    if hint:
        st.markdown(f'<p class="ks-field-hint">{hint}</p>', unsafe_allow_html=True)

    navn_soek = st.text_input(
        label,
        placeholder=placeholder,
        key=key_q,
    )
    q = navn_soek.strip()

    if len(q) < 2:
        existing = normalize_orgnr(str(st.session_state.get(output_session_key, "")))
        if is_valid_orgnr(existing):
            navn = ""
            if navn_session_key:
                navn = str(st.session_state.get(navn_session_key, "") or "").strip()
            name_label = html.escape(navn or "Valgt selskap")
            st.markdown(
                f"""
                <div class="ks-pick-banner ks-pick-banner-ok">
                    <strong>{name_label}</strong>
                    <span>Org.nr {existing}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            return
        st.session_state[output_session_key] = ""
        if navn_session_key:
            st.session_state[navn_session_key] = ""
        return

    try:
        client = BrregClient()
        treff = client.search_enheter_by_navn(q, size=15)
    except BrregError as exc:
        st.warning(f"Klarte ikke søke akkurat nå: {exc}")
        return

    if not treff:
        st.session_state[output_session_key] = ""
        if navn_session_key:
            st.session_state[navn_session_key] = ""
        st.markdown(
            f'<div class="ks-pick-banner ks-pick-banner-warn">Ingen treff på «{html.escape(q)}». Prøv et annet søkeord.</div>',
            unsafe_allow_html=True,
        )
        return

    labels = [format_company_hit(e) for e in treff]
    orgnr_list = [str(e.get("organisasjonsnummer", "")) for e in treff]

    picked_label = st.selectbox(
        "Velg firma fra forslagslista",
        options=labels,
        key=key_sb,
        help="Alle rader hentes live fra Brønnøysundregistrene.",
    )
    try:
        idx = labels.index(picked_label)
    except ValueError:
        idx = 0

    orgnr_val = normalize_orgnr(orgnr_list[idx])
    chosen = treff[idx]
    st.session_state[output_session_key] = orgnr_val
    if navn_session_key:
        st.session_state[navn_session_key] = str(chosen.get("navn", "") or "")

    suffix = f" {success_suffix}" if success_suffix else ""
    company_name = html.escape(str(chosen.get("navn", "?")))
    st.markdown(
        f"""
        <div class="ks-pick-banner ks-pick-banner-ok">
            <strong>{company_name}</strong>
            <span>Org.nr {orgnr_val}{suffix}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
