"""Landingsside og dashboard-komponenter."""

from __future__ import annotations

from typing import Any

from collections.abc import Callable

import base64
from pathlib import Path

import streamlit as st

from ui.styles import CUSTOM_CSS

BRAND_NAME = "B2B Scout"
LOGO_PATH = Path(__file__).resolve().parents[1] / "assets" / "logo.png"

EXAMPLE_DETAILS = [
    {
        "orgnr": "917537534",
        "name": "Hydro Aluminium",
        "industry": "Metall & industri",
        "icon": "🏭",
        "tag": "Konsern · MVA",
    },
    {
        "orgnr": "923609016",
        "name": "Equinor",
        "industry": "Energi & olje",
        "icon": "⚡",
        "tag": "Børsnotert · Konsern",
    },
    {
        "orgnr": "984661185",
        "name": "Posten Bring",
        "industry": "Logistikk & post",
        "icon": "📦",
        "tag": "9 000+ ansatte",
    },
    {
        "orgnr": "935917093",
        "name": "Schibsted",
        "industry": "Media & tech",
        "icon": "📰",
        "tag": "Digital vekst",
    },
]


def inject_styles() -> None:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def _logo_data_uri() -> str:
    if not LOGO_PATH.exists():
        return ""
    data = LOGO_PATH.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:image/png;base64,{b64}"


def render_landing_hero() -> None:
    logo_uri = _logo_data_uri()
    st.markdown(
        f"""
        <div class="ks-landing-hero">
            <div class="ks-landing-brand">
                {'<img class="ks-brand-logo" src="' + logo_uri + '" alt="B2B Scout logo" />' if logo_uri else '<div class="ks-brand-fallback">B2B</div>'}
                <div>
                    <div class="ks-brand-name">{BRAND_NAME}</div>
                    <div class="ks-landing-badge">Salgsintelligens for norske B2B-team</div>
                </div>
            </div>
            <h1 class="ks-landing-headline">
                Kjenn kunden bedre<br>
                <span class="ks-landing-accent">før du tar kontakt</span>
            </h1>
            <p class="ks-landing-lead">
                Søk opp et prospekt og få en ferdig salgsbrief — Brreg, regnskap,
                nyheter og AI-genererte kjøpssignaler samlet på ett sted.
            </p>
            <div class="ks-landing-stats">
                <div class="ks-landing-stat">
                    <strong>2M+</strong>
                    <span>Norske selskaper</span>
                </div>
                <div class="ks-landing-stat">
                    <strong>3</strong>
                    <span>Nyhetsartikler</span>
                </div>
                <div class="ks-landing-stat">
                    <strong>&lt;30s</strong>
                    <span>Til ferdig brief</span>
                </div>
                <div class="ks-landing-stat">
                    <strong>7</strong>
                    <span>Salgsseksjoner</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_landing_search_box() -> None:
    st.markdown(
        """
        <div class="ks-form-panel-head">
            <div class="ks-form-panel-title">Start analysen</div>
            <div class="ks-form-panel-sub">
                Tre enkle steg — bare kunden er påkrevd. Resten gjør briefen skarpere.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_form_section_title(
    step: int | str,
    title: str,
    subtitle: str = "",
    *,
    badge: str | None = None,
) -> None:
    badge_html = ""
    if badge == "optional":
        badge_html = '<span class="ks-form-pill ks-form-pill-optional">Valgfritt</span>'
    elif badge == "required":
        badge_html = '<span class="ks-form-pill ks-form-pill-required">Påkrevd</span>'

    sub = f'<div class="ks-form-section-sub">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f"""
        <div class="ks-form-section">
            <div class="ks-form-section-head">
                <div class="ks-step-icon">{step}</div>
                <div class="ks-form-section-copy">
                    <div class="ks-form-section-title">{title} {badge_html}</div>
                    {sub}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_form_footer_note() -> None:
    st.markdown(
        """
        <div class="ks-form-footer-note">
            <strong>Kunden</strong> må velges. <strong>Ditt selskap</strong> og
            <strong>produkt</strong> er valgfrie — hver for seg eller sammen.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_feature_grid() -> None:
    st.markdown(
        """
        <div class="ks-landing-section">
            <div class="ks-landing-section-title">Alt du trenger for å ta en smartere samtale</div>
            <div class="ks-feature-grid">
                <div class="ks-feature-card">
                    <div class="ks-feature-icon">🏛️</div>
                    <div class="ks-feature-title">Brreg i sanntid</div>
                    <div class="ks-feature-desc">
                        Org.form, ansatte, bransje, kapital, roller og risikoflag —
                        hentet direkte fra Enhetsregisteret.
                    </div>
                </div>
                <div class="ks-feature-card">
                    <div class="ks-feature-icon">📰</div>
                    <div class="ks-feature-title">Dagsaktuelle nyheter</div>
                    <div class="ks-feature-desc">
                        De 3 nyeste artiklene om selskapet fra Google News og NewsAPI —
                        investeringer, resultater, kontrakter.
                    </div>
                </div>
                <div class="ks-feature-card">
                    <div class="ks-feature-icon">📊</div>
                    <div class="ks-feature-title">Regnskapstall</div>
                    <div class="ks-feature-desc">
                        Omsetning, driftsresultat og egenkapital fra Regnskapsregisteret —
                        AI vurderer kjøpskapasitet før den pitcher.
                    </div>
                </div>
                <div class="ks-feature-card">
                    <div class="ks-feature-icon">🎯</div>
                    <div class="ks-feature-title">Ditt selskap + tilbud</div>
                    <div class="ks-feature-desc">
                        Velg ditt selskap som hovedkontekst, og evt. hva du selger som tillegg —
                        AI tilpasser posisjonering, produktmatch og pitch.
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_how_it_works() -> None:
    st.markdown(
        """
        <div class="ks-landing-section">
            <div class="ks-landing-section-title">Slik fungerer det</div>
            <div class="ks-steps">
                <div class="ks-step">
                    <div class="ks-step-num">1</div>
                    <div class="ks-step-title">Ditt selskap</div>
                    <div class="ks-step-desc">Valgfritt hovedfelt — søk firmanavn eller org.nr for posisjonering.</div>
                </div>
                <div class="ks-step-arrow">→</div>
                <div class="ks-step">
                    <div class="ks-step-num">2</div>
                    <div class="ks-step-title">Velg kunden</div>
                    <div class="ks-step-desc">Påkrevd prospekt — vi henter Brreg, regnskap og nyheter.</div>
                </div>
                <div class="ks-step-arrow">→</div>
                <div class="ks-step">
                    <div class="ks-step-num">3</div>
                    <div class="ks-step-title">Få salgsbrief</div>
                    <div class="ks-step-desc">AI leverer profil, økonomi, produktmatch og neste steg — klart til bruk.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_example_companies(on_select: Callable[[str], None] | None = None) -> None:
    st.markdown(
        """
        <div class="ks-landing-section">
            <div class="ks-landing-section-title">Prøv med et eksempel</div>
            <div class="ks-landing-section-sub">Klikk et selskap for å se en full analyse med en gang</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(4)
    for col, company in zip(cols, EXAMPLE_DETAILS):
        with col:
            st.markdown(
                f"""
                <div class="ks-example-card">
                    <div class="ks-example-icon">{company["icon"]}</div>
                    <div class="ks-example-name">{company["name"]}</div>
                    <div class="ks-example-industry">{company["industry"]}</div>
                    <div class="ks-example-tag">{company["tag"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            btn_kwargs: dict = {
                "key": f"landing_{company['orgnr']}",
                "use_container_width": True,
            }
            if on_select:
                btn_kwargs["on_click"] = on_select
                btn_kwargs["args"] = (company["orgnr"],)

            st.button(f"Analyser {company['name']}", **btn_kwargs)


def render_output_preview() -> None:
    st.markdown(
        """
        <div class="ks-landing-section">
            <div class="ks-landing-section-title">Dette får du i rapporten</div>
            <div class="ks-preview-grid">
                <div class="ks-preview-item">
                    <div class="ks-preview-label">Økonomisk helse</div>
                    <div class="ks-preview-text">Omsetning, driftsresultat og kjøpskapasitet vurdert før pitch</div>
                </div>
                <div class="ks-preview-item ks-preview-highlight">
                    <div class="ks-preview-label">⚡ Produktmatch</div>
                    <div class="ks-preview-text">Basert på ditt selskap og/eller hva du selger</div>
                </div>
                <div class="ks-preview-item ks-preview-highlight">
                    <div class="ks-preview-label">Kjøpssignaler</div>
                    <div class="ks-preview-text">Dagsaktuelle nyheter + Brreg koblet til din kontekst</div>
                </div>
                <div class="ks-preview-item">
                    <div class="ks-preview-label">Beslutningstaker</div>
                    <div class="ks-preview-text">Hvem du bør kontakte først — fra Brreg roller</div>
                </div>
                <div class="ks-preview-item">
                    <div class="ks-preview-label">Samtalevinkler</div>
                    <div class="ks-preview-text">3 icebreakers tilpasset din kontekst</div>
                </div>
                <div class="ks-preview-item">
                    <div class="ks-preview-label">Neste steg</div>
                    <div class="ks-preview-text">Én konkret handling for selgeren denne uken</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_trust_bar() -> None:
    st.markdown(
        """
        <div class="ks-trust-bar">
            <span>Datakilder:</span>
            <span class="ks-trust-pill">Brønnøysundregistrene</span>
            <span class="ks-trust-pill">Google News</span>
            <span class="ks-trust-pill">Regnskapsregisteret</span>
            <span class="ks-trust-pill">Grok / Groq AI</span>
            <span class="ks-trust-note">· NLOD-lisens · AI bør verifiseres før bruk i salg</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_landing_page() -> None:
    """Full landingsside — kalles når ingen analyse er aktiv."""
    render_landing_hero()
    render_landing_search_box()
    render_feature_grid()
    render_how_it_works()
    render_example_companies()
    render_output_preview()
    render_trust_bar()


# ── Dashboard-komponenter (resultatvisning) ──


def render_topbar() -> None:
    logo_uri = _logo_data_uri()
    st.markdown(
        f"""
        <div class="ks-topbar">
            <div class="ks-topbar-left">
                {'<img class="ks-topbar-logo" src="' + logo_uri + '" alt="logo" />' if logo_uri else '<div class="ks-topbar-logo-fallback">B2B</div>'}
                <div>
                    <div class="ks-topbar-title">{BRAND_NAME}</div>
                    <div class="ks-topbar-sub">Salgsbrief generert</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_company_bar(summary: dict[str, Any], orgnr: str) -> None:
    badges_html = _badges_html(summary)
    st.markdown(
        f"""
        <div class="ks-company-bar">
            <div>
                <div class="ks-company-name">{summary.get("navn", "Ukjent")}</div>
                <div class="ks-company-meta">Org.nr {orgnr} · {summary.get("organisasjonsform", "")}</div>
            </div>
            {badges_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _badges_html(summary: dict[str, Any]) -> str:
    badges: list[tuple[str, str]] = []
    if summary.get("konkurs"):
        badges.append(("danger", "Konkurs"))
    elif summary.get("under_avvikling"):
        badges.append(("warn", "Avvikling"))
    else:
        badges.append(("ok", "Aktiv"))
    if summary.get("mva_registrert"):
        badges.append(("ok", "MVA"))
    if summary.get("er_i_konsern"):
        badges.append(("neutral", "Konsern"))
    if summary.get("foretaksregisteret"):
        badges.append(("ok", "Foretaksreg."))
    html = '<div class="ks-badges">'
    for kind, label in badges:
        html += f'<span class="ks-badge ks-badge-{kind}">{label}</span>'
    html += "</div>"
    return html


def _format_number(value: Any) -> str:
    if value is None:
        return "–"
    try:
        return f"{int(value):,}".replace(",", " ")
    except (TypeError, ValueError):
        return str(value)


def _format_nok_short(value: Any) -> str:
    if value is None:
        return "–"
    try:
        amount = float(value)
    except (TypeError, ValueError):
        return str(value)
    if abs(amount) >= 1_000_000_000:
        return f"{amount / 1_000_000_000:.1f} mrd"
    if abs(amount) >= 1_000_000:
        return f"{amount / 1_000_000:,.0f} MNOK".replace(",", " ")
    return f"{amount:,.0f}".replace(",", " ")


def render_metrics_strip(summary: dict[str, Any]) -> None:
    regnskap = summary.get("regnskap") or {}
    if regnskap.get("omsetning_nok"):
        metrics = [
            ("Omsetning", _format_nok_short(regnskap.get("omsetning_nok"))),
            ("Driftsresultat", _format_nok_short(regnskap.get("driftsresultat_nok"))),
            ("Ansatte", _format_number(summary.get("antall_ansatte"))),
            (f"Regnskap {regnskap.get('regnskapsaar', '')}", _format_nok_short(regnskap.get("egenkapital_nok")) + " EK"),
        ]
    else:
        metrics = [
            ("Ansatte", _format_number(summary.get("antall_ansatte"))),
            ("Aksjekapital", f"{_format_number(summary.get('aksjekapital_nok'))} kr"),
            ("Stiftet", summary.get("stiftelsesdato") or "–"),
            ("Årsregnskap", summary.get("siste_arsregnskap") or "–"),
        ]
    cells = "".join(
        f'<div class="ks-metric"><div class="ks-metric-label">{l}</div>'
        f'<div class="ks-metric-value">{v}</div></div>'
        for l, v in metrics
    )
    st.markdown(f'<div class="ks-metrics-row">{cells}</div>', unsafe_allow_html=True)


def render_financial_panel(summary: dict[str, Any]) -> None:
    regnskap = summary.get("regnskap")
    if not regnskap:
        return

    rows = [
        ("Omsetning", _format_nok_short(regnskap.get("omsetning_nok")) + " NOK"),
        ("Driftsresultat", _format_nok_short(regnskap.get("driftsresultat_nok")) + " NOK"),
        ("Årsresultat", _format_nok_short(regnskap.get("aarsresultat_nok")) + " NOK"),
        ("Egenkapital", _format_nok_short(regnskap.get("egenkapital_nok")) + " NOK"),
        ("Gjeld", _format_nok_short(regnskap.get("sum_gjeld_nok")) + " NOK"),
    ]
    rows_html = "".join(
        f'<div class="ks-row"><span class="ks-row-label">{l}</span>'
        f'<span class="ks-row-value">{v}</span></div>'
        for l, v in rows
    )
    st.markdown(
        f'<div class="ks-panel"><div class="ks-panel-title">📊 Regnskap {regnskap.get("regnskapsaar", "")}</div>{rows_html}</div>',
        unsafe_allow_html=True,
    )


def render_news_compact(articles: list[dict[str, Any]], source_label: str) -> None:
    st.markdown(
        f'<div class="ks-panel"><div class="ks-panel-title">📰 Nyheter · {source_label}</div>',
        unsafe_allow_html=True,
    )
    if not articles:
        st.markdown(
            '<p style="margin:0;font-size:0.78rem;color:#64748B;">Ingen artikler funnet.</p></div>',
            unsafe_allow_html=True,
        )
        return
    items = ""
    for article in articles:
        title = article.get("title", "Ukjent")
        source = article.get("source", "")
        published = article.get("published", "")
        url = article.get("url", "")
        link = f'<a class="ks-news-link" href="{url}" target="_blank">Les →</a>' if url else ""
        items += f"""
        <div class="ks-news-item">
            <div class="ks-news-title">{title}</div>
            <div class="ks-news-meta">{source} · {published} {link}</div>
        </div>
        """
    st.markdown(items + "</div>", unsafe_allow_html=True)


def render_info_panel(summary: dict[str, Any]) -> None:
    rows = [
        ("Bransje", summary.get("naeringskode1", "–")),
        ("Adresse", summary.get("forretningsadresse", "–")),
        ("Ansatte", _format_number(summary.get("antall_ansatte"))),
        ("MVA", "Ja" if summary.get("mva_registrert") else "Nei"),
        ("Konsern", "Ja" if summary.get("er_i_konsern") else "Nei"),
    ]
    rows_html = "".join(
        f'<div class="ks-row"><span class="ks-row-label">{l}</span>'
        f'<span class="ks-row-value">{v}</span></div>'
        for l, v in rows
    )
    st.markdown(
        f'<div class="ks-panel"><div class="ks-panel-title">Selskap</div>{rows_html}</div>',
        unsafe_allow_html=True,
    )


def render_roles_compact(roles: list[str], max_items: int = 5) -> None:
    st.markdown(
        '<div class="ks-panel"><div class="ks-panel-title">Nøkkelpersoner</div>',
        unsafe_allow_html=True,
    )
    if not roles:
        st.markdown('<p style="margin:0;font-size:0.76rem;color:#64748B;">Ingen roller.</p></div>', unsafe_allow_html=True)
        return
    items = "".join(f'<div class="ks-role">{r}</div>' for r in roles[:max_items])
    if len(roles) > max_items:
        items += f'<div class="ks-role" style="color:#64748B;">+ {len(roles) - max_items} til</div>'
    st.markdown(items + "</div>", unsafe_allow_html=True)


def render_full_info_cards(summary: dict[str, Any]) -> None:
    col1, col2 = st.columns(2)
    fields_left = [
        ("Org.nr", summary.get("organisasjonsnummer")),
        ("Form", summary.get("organisasjonsform")),
        ("Stiftet", summary.get("stiftelsesdato")),
        ("Registrert", summary.get("registreringsdato")),
        ("Sektor", summary.get("institusjonell_sektor")),
    ]
    fields_right = [
        ("Bransje 2", summary.get("naeringskode2")),
        ("Bransje 3", summary.get("naeringskode3")),
        ("Konkurs", "Ja" if summary.get("konkurs") else "Nei"),
        ("Aksjekapital", f"{_format_number(summary.get('aksjekapital_nok'))} kr"),
    ]
    with col1:
        for label, val in fields_left:
            st.caption(f"**{label}:** {val or '–'}")
    with col2:
        for label, val in fields_right:
            st.caption(f"**{label}:** {val or '–'}")
    aktivitet = summary.get("aktivitet")
    if aktivitet:
        st.caption(f"**Aktivitet:** {aktivitet[:300]}{'…' if len(aktivitet) > 300 else ''}")


def render_footer() -> None:
    st.markdown(
        f'<div class="ks-footer">Brreg (NLOD) · Google News / NewsAPI · {BRAND_NAME}</div>',
        unsafe_allow_html=True,
    )
