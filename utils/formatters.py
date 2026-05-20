"""Formatering av Brreg JSON til menneskelesbar og AI-vennlig tekst."""

from __future__ import annotations

from typing import Any


def _get_nested(data: dict[str, Any], *keys: str, default: Any = None) -> Any:
    """Hent verdi fra nested dict uten KeyError."""
    current: Any = data
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key, default)
        if current is default:
            return default
    return current


def _format_address(address: dict[str, Any] | None) -> str:
    """Konverter adresse-objekt til én lesbar streng."""
    if not address:
        return "Ikke oppgitt"

    street = ", ".join(address.get("adresse", []))
    post = f"{address.get('postnummer', '')} {address.get('poststed', '')}".strip()
    kommune = address.get("kommune", "")

    parts = [part for part in (street, post, kommune) if part]
    return ", ".join(parts) if parts else "Ikke oppgitt"


def _format_code_object(obj: dict[str, Any] | None) -> str:
    """
    Mange Brreg-felt er objekter med kode + beskrivelse.

    Eksempel: {"kode": "AS", "beskrivelse": "Aksjeselskap"}
    """
    if not obj:
        return "Ikke oppgitt"
    kode = obj.get("kode", "")
    beskrivelse = obj.get("beskrivelse", "")
    if kode and beskrivelse:
        return f"{kode} – {beskrivelse}"
    return beskrivelse or kode or "Ikke oppgitt"


def _format_roles(roller_data: dict[str, Any] | None) -> list[str]:
    """
    Flat ut rollegrupper til en liste med strenger.

    Brreg-struktur:
    rollegrupper[] → type (f.eks. "Styre") → roller[] → person/enhet + rolletype
    """
    if not roller_data:
        return []

    lines: list[str] = []
    for gruppe in roller_data.get("rollegrupper", []):
        gruppe_navn = _get_nested(gruppe, "type", "beskrivelse", default="Ukjent gruppe")

        for rolle in gruppe.get("roller", []):
            if rolle.get("fratraadt") or rolle.get("avregistrert"):
                continue

            rolle_navn = _get_nested(rolle, "type", "beskrivelse", default="Ukjent rolle")

            # Personroller (daglig leder, styremedlem)
            if "person" in rolle:
                navn_obj = rolle["person"].get("navn", {})
                fornavn = navn_obj.get("fornavn", "")
                mellomnavn = navn_obj.get("mellomnavn", "")
                etternavn = navn_obj.get("etternavn", "")
                fullt_navn = " ".join(part for part in (fornavn, mellomnavn, etternavn) if part)
                lines.append(f"{rolle_navn} ({gruppe_navn}): {fullt_navn}")

            # Enhetsroller (revisor, eier som selskap)
            elif "enhet" in rolle:
                enhet = rolle["enhet"]
                navn_liste = enhet.get("navn", [])
                navn = navn_liste[0] if navn_liste else "Ukjent enhet"
                orgnr = enhet.get("organisasjonsnummer", "")
                lines.append(f"{rolle_navn} ({gruppe_navn}): {navn} ({orgnr})")

    return lines


def build_company_summary(
    enhet: dict[str, Any],
    roller: dict[str, Any] | None,
    regnskap: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Trekk ut de viktigste feltene fra rå Brreg-JSON.

    Dette er "broen" mellom Brregs komplekse API-respons og AI-prompten.
    Vi velger bevisst salgsrelevante felt og ignorerer metadata (_links).
    """
    kapital = enhet.get("kapital") or {}

    return {
        "organisasjonsnummer": enhet.get("organisasjonsnummer"),
        "navn": enhet.get("navn"),
        "organisasjonsform": _format_code_object(enhet.get("organisasjonsform")),
        "stiftelsesdato": enhet.get("stiftelsesdato"),
        "registreringsdato": enhet.get("registreringsdatoEnhetsregisteret"),
        "naeringskode1": _format_code_object(enhet.get("naeringskode1")),
        "naeringskode2": _format_code_object(enhet.get("naeringskode2")),
        "naeringskode3": _format_code_object(enhet.get("naeringskode3")),
        "antall_ansatte": enhet.get("antallAnsatte"),
        "forretningsadresse": _format_address(enhet.get("forretningsadresse")),
        "postadresse": _format_address(enhet.get("postadresse")),
        "mva_registrert": enhet.get("registrertIMvaregisteret"),
        "foretaksregisteret": enhet.get("registrertIForetaksregisteret"),
        "konkurs": enhet.get("konkurs"),
        "under_avvikling": enhet.get("underAvvikling"),
        "siste_arsregnskap": enhet.get("sisteInnsendteAarsregnskap"),
        "er_i_konsern": enhet.get("erIKonsern"),
        "institusjonell_sektor": _format_code_object(enhet.get("institusjonellSektorkode")),
        "aksjekapital_nok": kapital.get("belop"),
        "aktivitet": " ".join(enhet.get("aktivitet", [])),
        "vedtektsfestet_formaal": " ".join(enhet.get("vedtektsfestetFormaal", [])),
        "roller": _format_roles(roller),
        "regnskap": regnskap,
    }


def _format_nok(value: Any) -> str:
    """Formater NOK-beløp lesbart for AI og UI."""
    if value is None:
        return "Ikke tilgjengelig"
    try:
        amount = float(value)
    except (TypeError, ValueError):
        return str(value)

    if abs(amount) >= 1_000_000_000:
        return f"{amount / 1_000_000_000:.1f} mrd NOK"
    if abs(amount) >= 1_000_000:
        return f"{amount / 1_000_000:,.0f} MNOK".replace(",", " ")
    return f"{amount:,.0f} NOK".replace(",", " ")


def regnskap_to_prompt_text(regnskap: dict[str, Any] | None) -> str:
    """Formater regnskapstall for AI-prompten."""
    if not regnskap:
        return """
Regnskapstall (Regnskapsregisteret):
Ingen årsregnskap funnet. Vurder økonomisk helse basert på Brreg-data (kapital, konkurs, ansatte).
""".strip()

    return f"""
Regnskapstall (Regnskapsregisteret, regnskapsår {regnskap.get('regnskapsaar', 'ukjent')}):

Periode: {regnskap.get('periode_fra')} – {regnskap.get('periode_til')}
Omsetning (sum driftsinntekter): {_format_nok(regnskap.get('omsetning_nok'))}
Driftsresultat: {_format_nok(regnskap.get('driftsresultat_nok'))}
Årsresultat: {_format_nok(regnskap.get('aarsresultat_nok'))}
Sum eiendeler: {_format_nok(regnskap.get('sum_eiendeler_nok'))}
Egenkapital: {_format_nok(regnskap.get('egenkapital_nok'))}
Sum gjeld: {_format_nok(regnskap.get('sum_gjeld_nok'))}
""".strip()


def seller_product_to_prompt_text(seller_product: str) -> str:
    """Selgerens produkt — tilleggsinfo som spisser analysen."""
    product = seller_product.strip()
    if not product:
        return """
Selgerens produkt/tjeneste: Ikke oppgitt.
Basér produktmatch på selgerens selskap (hvis oppgitt) og kundens data.
""".strip()

    return f"""
Selgerens produkt/tjeneste (tilleggsinfo — spisser pitch og produktmatch):
{product}

Instruks: Koble produktet til kundens bransje, størrelse, økonomi og nyheter.
""".strip()


def seller_company_to_prompt_text(seller_company: dict[str, Any] | None) -> str:
    """
    Selgerens eget selskap (valgfritt) — brukes til å spisse posisjonering og mulige synergier.

    Hvis dette er satt, kan modellen:
    - bruke bransje/størrelse til å foreslå relevant pitch-vinkel
    - foreslå «andre muligheter» (partnerskap, konserninnsalg, tilleggstjenester)
    """
    if not seller_company:
        return """
Selgerens selskap: Ikke oppgitt.
Bruk produktbeskrivelsen (hvis oppgitt) som hovedgrunnlag for posisjonering.
""".strip()

    regnskap = seller_company.get("regnskap") or {}
    regnskap_tekst = ""
    if regnskap.get("omsetning_nok"):
        regnskap_tekst = f"""
Selgerens regnskap ({regnskap.get('regnskapsaar', '')}):
Omsetning: {_format_nok(regnskap.get('omsetning_nok'))}
Driftsresultat: {_format_nok(regnskap.get('driftsresultat_nok'))}
"""

    aktivitet = (seller_company.get("aktivitet") or "").strip()
    formaal = (seller_company.get("vedtektsfestet_formaal") or "").strip()
    virksomhet = aktivitet or formaal or "Ikke oppgitt i Brreg"
    if aktivitet and formaal and formaal not in aktivitet:
        virksomhet = f"{aktivitet}\n\nVedtektsfestet formål: {formaal}"

    roller = seller_company.get("roller") or []
    roller_tekst = "\n".join(f"- {r}" for r in roller[:8]) if roller else "Ingen roller listet"

    return f"""
Selgerens selskap (HOVEDKONTEKST — hvem du representerer):
Navn: {seller_company.get('navn')}
Org.nr: {seller_company.get('organisasjonsnummer')}
Organisasjonsform: {seller_company.get('organisasjonsform')}

Hva selgerens firma driver med (Brreg):
{virksomhet}

Bransje (næringskode): {seller_company.get('naeringskode1')}
Næringskode 2: {seller_company.get('naeringskode2')}
Ansatte: {seller_company.get('antall_ansatte')}
Konsern: {seller_company.get('er_i_konsern')}
Nøkkelroller:
{roller_tekst}
{regnskap_tekst}

Instruks: Bruk «Hva selgerens firma driver med» som grunnlag for produktmatch og posisjonering.
Ikke skriv at selgerens selskap mangler når denne seksjonen er fylt ut.
""".strip()


def summary_to_prompt_text(
    summary: dict[str, Any],
    news_articles: list[dict[str, Any]] | None = None,
    seller_product: str = "",
    seller_company: dict[str, Any] | None = None,
) -> str:
    """Bygg komplett user-prompt med alle datakilder."""
    roller = summary.get("roller") or ["Ingen aktive roller funnet"]
    roller_tekst = "\n".join(f"- {r}" for r in roller)

    seller_section = seller_product_to_prompt_text(seller_product)
    seller_company_section = seller_company_to_prompt_text(seller_company)
    regnskap_section = regnskap_to_prompt_text(summary.get("regnskap"))
    news_section = news_to_prompt_text(news_articles or [])

    brreg_section = f"""
Selskapsdata fra Brønnøysundregistrene:

Navn: {summary.get('navn')}
Org.nr: {summary.get('organisasjonsnummer')}
Organisasjonsform: {summary.get('organisasjonsform')}
Stiftet: {summary.get('stiftelsesdato')}
Registrert i Enhetsregisteret: {summary.get('registreringsdato')}

Bransje (næringskode 1): {summary.get('naeringskode1')}
Næringskode 2: {summary.get('naeringskode2')}
Næringskode 3: {summary.get('naeringskode3')}

Antall ansatte: {summary.get('antall_ansatte')}
Forretningsadresse: {summary.get('forretningsadresse')}
MVA-registrert: {summary.get('mva_registrert')}
I foretaksregisteret: {summary.get('foretaksregisteret')}
Siste innsendte årsregnskap: {summary.get('siste_arsregnskap')}
Del av konsern: {summary.get('er_i_konsern')}
Institusjonell sektor: {summary.get('institusjonell_sektor')}
Aksjekapital (NOK): {summary.get('aksjekapital_nok')}

Konkurs: {summary.get('konkurs')}
Under avvikling: {summary.get('under_avvikling')}

Aktivitetsbeskrivelse:
{summary.get('aktivitet')}

Vedtektsfestet formål:
{summary.get('vedtektsfestet_formaal')}

Nøkkelpersoner og roller:
{roller_tekst}
""".strip()

    return "\n\n".join(
        [seller_company_section, seller_section, brreg_section, regnskap_section, news_section]
    )


def news_to_prompt_text(articles: list[dict[str, Any]]) -> str:
    """Formater nyhetsartikler for AI-prompten."""
    if not articles:
        return """
Dagsaktuelle nyheter (siste 30 dager):
Ingen relevante artikler funnet. Basér kjøpssignaler primært på Brreg-data.
""".strip()

    lines = ["Dagsaktuelle nyheter (siste 30 dager):", ""]
    for i, article in enumerate(articles, start=1):
        lines.append(f"Artikkel {i}:")
        lines.append(f"  Tittel: {article.get('title', 'Ukjent')}")
        lines.append(f"  Kilde: {article.get('source', 'Ukjent')}")
        lines.append(f"  Dato: {article.get('published', 'Ukjent')}")
        lines.append(f"  Sammendrag: {article.get('summary', 'Ingen')}")
        lines.append("")

    return "\n".join(lines).strip()
