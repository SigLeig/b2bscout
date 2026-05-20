"""
B2B Scout – B2B salgsanalyse fra Brreg-data.
"""



from __future__ import annotations



import streamlit as st



from config import settings

from services.ai_analysis import AIAnalysisError, generate_sales_analysis

from services.brreg import BrregClient, BrregError, BrregNotFoundError

from services.news import NewsFetchError, articles_to_dicts, fetch_company_news

from services.regnskap import fetch_regnskap_summary

from ui.company_search import SESSION_KEY_SELECTED_ORGNR, render_company_autocomplete

from ui.components import (

    inject_styles,

    render_company_bar,

    render_example_companies,

    render_feature_grid,

    render_financial_panel,

    render_footer,

    render_form_section_title,

    render_form_footer_note,

    render_full_info_cards,

    render_how_it_works,

    render_info_panel,

    render_landing_hero,

    render_landing_search_box,

    render_metrics_strip,

    render_news_compact,

    render_output_preview,

    render_roles_compact,

    render_topbar,

    render_trust_bar,

)

from utils.formatters import build_company_summary, summary_to_prompt_text

from utils.orgnr import is_valid_orgnr, normalize_orgnr



st.set_page_config(
    page_title="B2B Scout",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)



inject_styles()



if "last_result" not in st.session_state:

    st.session_state.last_result = None



if "seller_product" not in st.session_state:

    st.session_state.seller_product = ""





def _resolve_orgnr() -> str:

    """Direkte org.nr overstyrer valg fra firmanavn-søket (kunde)."""

    manual = normalize_orgnr(st.session_state.get("orgnr_input", ""))

    picked = normalize_orgnr(str(st.session_state.get(SESSION_KEY_SELECTED_ORGNR, "")))



    if is_valid_orgnr(manual):

        return manual

    if is_valid_orgnr(picked):

        return picked

    last = st.session_state.get("last_result") or {}
    cached = normalize_orgnr(str(last.get("orgnr", "")))
    if is_valid_orgnr(cached):
        return cached

    return ""





def _resolve_seller_company_orgnr() -> str:

    """Direkte org.nr overstyrer valg fra firmanavn-søket (selger)."""

    manual = normalize_orgnr(st.session_state.get("seller_company_orgnr_manual", ""))

    picked = normalize_orgnr(st.session_state.get("seller_company_orgnr", ""))



    if is_valid_orgnr(manual):

        return manual

    if is_valid_orgnr(picked):

        return picked

    # Behold valg fra forrige analyse hvis søkefeltet ble tømt ved visningsbytte (landing → dash)
    last = st.session_state.get("last_result") or {}
    cached = normalize_orgnr(str(last.get("seller_company_orgnr", "")))
    if is_valid_orgnr(cached):
        return cached

    return ""





def _fetch_seller_company_summary(client: BrregClient, orgnr: str) -> dict | None:

    try:

        sel_enhet, sel_roller = client.fetch_company_bundle(orgnr)

        return build_company_summary(

            sel_enhet, sel_roller, regnskap=fetch_regnskap_summary(orgnr)

        )

    except (BrregError, BrregNotFoundError):

        return None





def _select_example(orgnr: str) -> None:

    """Callback — må brukes med on_click."""

    st.session_state.orgnr_input = orgnr

    st.session_state[SESSION_KEY_SELECTED_ORGNR] = normalize_orgnr(orgnr)

    st.session_state.auto_analyze = True





def _reset_search() -> None:

    st.session_state.last_result = None

    st.session_state.orgnr_input = ""

    st.session_state[SESSION_KEY_SELECTED_ORGNR] = ""

    st.session_state.seller_company_orgnr = ""

    st.session_state.seller_company_orgnr_manual = ""
    st.session_state.seller_company_navn = ""





def _provider_config(provider: str) -> tuple[bool, str]:

    if provider == "groq":

        return bool(settings.groq_api_key), settings.groq_model

    if provider == "grok":

        return bool(settings.xai_api_key), settings.xai_model

    return bool(settings.openrouter_api_key), settings.openrouter_model





def _render_sidebar() -> str:

    with st.sidebar:

        st.markdown('<div class="ks-sidebar-brand">⚙️ Innstillinger</div>', unsafe_allow_html=True)



        provider_options = ["groq", "grok", "openrouter"]

        if "provider" not in st.session_state:

            st.session_state.provider = (

                settings.provider if settings.provider in provider_options else "grok"

            )

        provider = st.selectbox("AI-leverandør", provider_options, label_visibility="collapsed", key="provider")



        api_ok, model_name = _provider_config(provider)

        st.caption(f"Modell: `{model_name}`")

        pill_class = "ks-status-ok" if api_ok else "ks-status-warn"

        pill_text = "API aktiv" if api_ok else "API mangler"

        st.markdown(f'<div class="ks-status-pill {pill_class}">● {pill_text}</div>', unsafe_allow_html=True)



        st.button("← Nytt søk", use_container_width=True, on_click=_reset_search)



    return provider





def _render_analysis_form(fragment_prefix: str, *, button_label: str) -> bool:

    """Skjema: ditt selskap (hoved) → produkt (tillegg) → kunde (påkrevd)."""

    render_form_section_title(
        1,
        "Ditt selskap",
        "Hvem du representerer — gir AI bedre posisjonering og troverdighet.",
        badge="optional",
    )

    render_company_autocomplete(
        f"{fragment_prefix}_seller",
        output_session_key="seller_company_orgnr",
        label="Firmanavn (ditt selskap)",
        placeholder="Skriv minst 2 tegn, f.eks. ditt eget firmanavn…",
        success_suffix="",
        navn_session_key="seller_company_navn",
    )

    with st.expander("Har du org.nr? Skriv det direkte"):
        st.text_input(
            "Org.nr for ditt selskap",
            key="seller_company_orgnr_manual",
            placeholder="9 siffer (valgfritt)",
        )

    render_form_section_title(
        2,
        "Hva selger du?",
        "Spisser pitch og produktmatch — kan brukes alene eller sammen med steg 1.",
        badge="optional",
    )

    with st.expander("Beskriv produkt eller tjeneste", expanded=False):
        st.text_area(
            "Produkt/tjeneste",
            placeholder="F.eks. «Skybasert CRM for B2B-salgsteam»",
            key="seller_product",
            height=80,
        )

    render_form_section_title(
        3,
        "Kunden (prospekt)",
        "Selskapet du vil analysere — dette er eneste påkrevde felt.",
        badge="required",
    )

    render_company_autocomplete(
        fragment_prefix,
        label="Firmanavn (kunde)",
        placeholder="Skriv minst 2 tegn, f.eks. Hydro, Equinor…",
        hint="Lista oppdateres mens du skriver.",
    )

    with st.expander("Har du org.nr? Skriv det direkte"):
        st.text_input(
            "Org.nr for kunden",
            placeholder="For eksempel 917537534",
            key="orgnr_input",
        )

    render_form_footer_note()

    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        return st.button(button_label, type="primary", use_container_width=True)





provider = _render_sidebar()



show_landing = not st.session_state.last_result and not st.session_state.get("auto_analyze")



analyze_clicked = False



if show_landing:

    _, main_col, _ = st.columns([1, 6, 1])

    with main_col:

        render_landing_hero()

        with st.container(border=True):

            render_landing_search_box()

            analyze_clicked = _render_analysis_form("landing", button_label="Analyser →")

        render_feature_grid()

        render_how_it_works()

        render_example_companies(on_select=_select_example)

        render_output_preview()

        render_trust_bar()

        render_footer()



    if not analyze_clicked:

        st.stop()



else:

    render_topbar()

    _, form_col, _ = st.columns([1, 5, 1])

    with form_col:

        with st.container(border=True):

            analyze_clicked = _render_analysis_form("dash", button_label="Analyser på nytt")



if analyze_clicked or st.session_state.pop("auto_analyze", False):

    orgnr_input_resolved = _resolve_orgnr()



    if not orgnr_input_resolved:

        st.error(

            "Velg **kunden** fra forslagslista (firmanavn), "

            "eller skriv inn et gyldig 9-sifret org.nr for prospektet."

        )

        render_footer()

        st.stop()



    seller_company_orgnr = _resolve_seller_company_orgnr()



    with st.spinner("Henter Brreg-data, regnskap og nyheter..."):

        try:

            client = BrregClient()

            enhet, roller = client.fetch_company_bundle(orgnr_input_resolved)

        except BrregNotFoundError:

            st.error(f"Fant ingen enhet med org.nr {orgnr_input_resolved}.")

            render_footer()

            st.stop()

        except BrregError as exc:

            st.error(f"Brreg-feil: {exc}")

            render_footer()

            st.stop()



        regnskap = fetch_regnskap_summary(orgnr_input_resolved)

        summary = build_company_summary(enhet, roller, regnskap=regnskap)



        seller_company_summary = None

        if is_valid_orgnr(seller_company_orgnr):

            seller_company_summary = _fetch_seller_company_summary(client, seller_company_orgnr)



        try:

            news_articles = fetch_company_news(summary["navn"], limit=3)

            news_source = (

                "NewsAPI"

                if settings.news_api_key and news_articles and news_articles[0].provider == "newsapi"

                else "Google News"

            )

        except NewsFetchError:

            news_articles = []

            news_source = "Ingen"



    st.session_state.last_result = {

        "orgnr": orgnr_input_resolved,

        "enhet": enhet,

        "roller": roller,

        "regnskap": regnskap,

        "summary": summary,

        "news": articles_to_dicts(news_articles),

        "news_source": news_source,

        "analysis": None,

        "provider": provider,

        "seller_product": st.session_state.get("seller_product", ""),

        "seller_company": seller_company_summary,

        "seller_company_orgnr": seller_company_orgnr,

    }

    st.rerun()



result = st.session_state.last_result

if not result:

    st.stop()



summary = result["summary"]

orgnr = result["orgnr"]

enhet = result["enhet"]

roller = result["roller"]

news = result.get("news", [])

news_source = result.get("news_source", "Google News")



render_company_bar(summary, orgnr)

render_metrics_strip(summary)



col_analysis, col_side = st.columns([3, 2], gap="small")



with col_side:

    render_financial_panel(summary)

    render_news_compact(news, news_source)

    render_info_panel(summary)

    render_roles_compact(summary["roller"])



    with st.expander("Mer selskapsdata"):

        render_full_info_cards(summary)

        for role in summary["roller"]:

            st.caption(f"• {role}")



    with st.expander("Rå JSON"):

        st.json(

            {

                "brreg": enhet,

                "roller": roller,

                "regnskap": result.get("regnskap"),

                "nyheter": news,

                "selger": {

                    "produkt": st.session_state.get("seller_product", ""),

                    "selskap": result.get("seller_company"),

                },

            },

            expanded=False,

        )



with col_analysis:

    seller_product = st.session_state.get("seller_product", "")

    seller_company = result.get("seller_company")

    seller_company_orgnr_current = _resolve_seller_company_orgnr()



    needs_new_analysis = (

        result.get("analysis") is None

        or result.get("provider") != provider

        or result.get("seller_product") != seller_product

        or result.get("seller_company_orgnr") != seller_company_orgnr_current

        or (

            is_valid_orgnr(seller_company_orgnr_current)

            and not result.get("seller_company")

        )

    )



    if needs_new_analysis:

        with st.spinner("Genererer salgsanalyse..."):

            try:

                seller_company = None
                if is_valid_orgnr(seller_company_orgnr_current):
                    client = BrregClient()
                    seller_company = _fetch_seller_company_summary(
                        client, seller_company_orgnr_current
                    )
                    st.session_state.seller_company_orgnr = seller_company_orgnr_current



                prompt_text = summary_to_prompt_text(

                    summary,

                    news_articles=news,

                    seller_product=seller_product,

                    seller_company=seller_company,

                )

                analysis = generate_sales_analysis(prompt_text, provider=provider)

                st.session_state.last_result["analysis"] = analysis

                st.session_state.last_result["provider"] = provider

                st.session_state.last_result["seller_product"] = seller_product

                st.session_state.last_result["seller_company"] = seller_company

                st.session_state.last_result["seller_company_orgnr"] = seller_company_orgnr_current

            except AIAnalysisError as exc:

                st.error(str(exc))

                render_footer()

                st.stop()



    analysis = st.session_state.last_result["analysis"]



    hdr_left, hdr_right = st.columns([4, 1])

    with hdr_left:

        st.markdown('<p class="ks-section-label">Salgsanalyse</p>', unsafe_allow_html=True)

    with hdr_right:

        st.download_button(

            "⬇ MD",

            data=analysis,

            file_name=f"b2b-scout_{orgnr}.md",

            mime="text/markdown",

            use_container_width=True,

        )



    with st.container(border=True):

        st.markdown(analysis)



render_footer()

