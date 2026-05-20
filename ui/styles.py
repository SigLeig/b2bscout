"""Global CSS – kompakt, arealeffektiv layout."""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --ks-primary: #1D4ED8;
    --ks-primary-dark: #1E3A8A;
    --ks-accent: #38BDF8;
    --ks-surface: #FFFFFF;
    --ks-text: #0F172A;
    --ks-text-soft: #334155;
    --ks-muted: #475569;
    --ks-border: #D7E0EC;
    --ks-panel: #F8FAFC;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    color: var(--ks-text);
}

.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(56, 189, 248, 0.14), transparent 55%),
        linear-gradient(180deg, #EEF4FF 0%, #F4F7FB 40%, #ECEFF4 100%);
}

#MainMenu, footer, header[data-testid="stHeader"] {
    visibility: hidden;
    height: 0;
}

.block-container {
    padding: 1rem 1.25rem 1.5rem 1.25rem;
    max-width: 100%;
}

div[data-testid="stVerticalBlock"] > div { gap: 0.55rem; }

/* Skjemakort (Streamlit container) */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.92) !important;
    border: 1px solid var(--ks-border) !important;
    border-radius: 18px !important;
    box-shadow: 0 14px 40px rgba(15, 23, 42, 0.07) !important;
    padding: 0.35rem 0.15rem !important;
    backdrop-filter: blur(6px);
}

label[data-testid="stWidgetLabel"] p,
label[data-testid="stWidgetLabel"] span {
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    color: var(--ks-text-soft) !important;
}

div[data-testid="stCaptionContainer"],
div[data-testid="stCaptionContainer"] p {
    color: var(--ks-text-soft) !important;
    font-size: 0.875rem !important;
    line-height: 1.55 !important;
}

/* ── Toppbar ── */
.ks-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
    border-radius: 10px;
    padding: 0.65rem 1rem;
    margin-bottom: 0.6rem;
}

.ks-topbar-left {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.ks-topbar-logo,
.ks-topbar-logo-fallback {
    width: 34px;
    height: 34px;
    border-radius: 9px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.18);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex: 0 0 auto;
}

.ks-topbar-logo {
    object-fit: contain;
    padding: 4px;
}

.ks-topbar-logo-fallback {
    font-size: 0.7rem;
    font-weight: 800;
    color: #fff;
    letter-spacing: -0.02em;
}

.ks-topbar-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #fff;
    white-space: nowrap;
}

.ks-topbar-sub {
    font-size: 0.72rem;
    color: #94A3B8;
    font-weight: 500;
}

/* ── Selskaps-header (kompakt) ── */
.ks-company-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.5rem 1rem;
    padding: 0.5rem 0;
    margin-bottom: 0.25rem;
    border-bottom: 1px solid var(--ks-border);
}

.ks-company-name {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--ks-text);
    margin: 0;
}

.ks-company-meta {
    font-size: 0.78rem;
    color: var(--ks-muted);
}

/* ── Badges (inline, små) ── */
.ks-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem;
    margin: 0;
}

.ks-badge {
    display: inline-flex;
    padding: 0.15rem 0.5rem;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 600;
    border: 1px solid transparent;
    white-space: nowrap;
}

.ks-badge-ok { background: #ECFDF5; color: #047857; border-color: #A7F3D0; }
.ks-badge-warn { background: #FFFBEB; color: #B45309; border-color: #FDE68A; }
.ks-badge-danger { background: #FEF2F2; color: #B91C1C; border-color: #FECACA; }
.ks-badge-neutral { background: #F8FAFC; color: #475569; border-color: #E2E8F0; }

/* ── Metrikk-stripe ── */
.ks-metrics-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}

.ks-metric {
    background: var(--ks-surface);
    border: 1px solid var(--ks-border);
    border-radius: 8px;
    padding: 0.45rem 0.65rem;
}

.ks-metric-label {
    font-size: 0.65rem;
    font-weight: 600;
    color: var(--ks-muted);
    text-transform: uppercase;
    letter-spacing: 0.03em;
}

.ks-metric-value {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--ks-text);
    line-height: 1.2;
}

/* ── Panel (høyre kolonne) ── */
.ks-panel {
    background: var(--ks-surface);
    border: 1px solid var(--ks-border);
    border-radius: 8px;
    padding: 0.65rem 0.75rem;
    margin-bottom: 0.5rem;
}

.ks-panel-title {
    font-size: 0.68rem;
    font-weight: 700;
    color: var(--ks-primary);
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin: 0 0 0.45rem 0;
    padding-bottom: 0.35rem;
    border-bottom: 1px solid var(--ks-border);
}

/* ── Nyhetsliste (kompakt) ── */
.ks-news-item {
    padding: 0.4rem 0;
    border-bottom: 1px solid #F1F5F9;
    font-size: 0.8rem;
    line-height: 1.4;
}

.ks-news-item:last-child { border-bottom: none; padding-bottom: 0; }

.ks-news-title {
    font-weight: 600;
    color: var(--ks-text);
    margin-bottom: 0.1rem;
}

.ks-news-meta {
    font-size: 0.68rem;
    color: var(--ks-muted);
}

.ks-news-link {
    font-size: 0.68rem;
    color: var(--ks-primary);
    text-decoration: none;
}

/* ── Info-rader (kompakt) ── */
.ks-row {
    display: flex;
    justify-content: space-between;
    gap: 0.5rem;
    padding: 0.2rem 0;
    font-size: 0.78rem;
    border-bottom: 1px solid #F8FAFC;
}

.ks-row:last-child { border-bottom: none; }
.ks-row-label { color: var(--ks-muted); }
.ks-row-value { color: var(--ks-text); font-weight: 600; text-align: right; max-width: 60%; }

/* ── Roller (kompakt) ── */
.ks-role {
    font-size: 0.76rem;
    color: var(--ks-text);
    padding: 0.15rem 0;
    border-bottom: 1px solid #F8FAFC;
    line-height: 1.35;
}

.ks-role:last-child { border-bottom: none; }

/* ── Analyse ── */
.ks-analysis-box {
    background: var(--ks-surface);
    border: 1px solid var(--ks-border);
    border-radius: 8px;
    padding: 0.85rem 1rem;
    font-size: 0.88rem;
    line-height: 1.55;
}

.ks-analysis-box h1, .ks-analysis-box h2, .ks-analysis-box h3 {
    font-size: 0.95rem;
    margin: 0.75rem 0 0.35rem 0;
}

.ks-section-label {
    font-size: 0.68rem;
    font-weight: 700;
    color: var(--ks-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin: 0 0 0.35rem 0;
}

/* ── Tom tilstand ── */
.ks-empty {
    text-align: center;
    padding: 2rem 1rem;
    background: var(--ks-surface);
    border: 1px dashed var(--ks-border);
    border-radius: 8px;
    color: var(--ks-muted);
    font-size: 0.85rem;
}

/* ══════════════════════════════════════
   LANDING PAGE
   ══════════════════════════════════════ */

.ks-landing-hero {
    background: linear-gradient(145deg, #0B1224 0%, #152C63 42%, #1D4ED8 78%, #2563EB 100%);
    border-radius: 20px;
    padding: 2rem 2.25rem 1.75rem;
    margin-bottom: 1.25rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 18px 50px rgba(15, 23, 42, 0.18);
}

.ks-landing-hero::before {
    content: "";
    position: absolute;
    top: -40%;
    right: -10%;
    width: 420px;
    height: 420px;
    background: radial-gradient(circle, rgba(96,165,250,0.18) 0%, transparent 70%);
    pointer-events: none;
}

.ks-landing-hero::after {
    content: "";
    position: absolute;
    bottom: -30%;
    left: 5%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(59,130,246,0.12) 0%, transparent 70%);
    pointer-events: none;
}

.ks-landing-badge {
    display: inline-block;
    background: rgba(56, 189, 248, 0.14);
    border: 1px solid rgba(125, 211, 252, 0.35);
    border-radius: 999px;
    padding: 0.35rem 0.9rem;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    text-transform: none;
    color: #E0F2FE;
    margin-bottom: 0;
}

.ks-landing-headline {
    font-size: 2.15rem;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.18;
    letter-spacing: -0.03em;
    margin: 1rem 0 0.75rem 0;
    max-width: 680px;
}

.ks-landing-accent {
    background: linear-gradient(90deg, #7DD3FC, #38BDF8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.ks-landing-lead {
    font-size: 1.02rem;
    color: #E2E8F0;
    line-height: 1.65;
    max-width: 620px;
    margin: 0 0 1.5rem 0;
}

.ks-landing-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem 2.5rem;
}

.ks-landing-stat {
    display: flex;
    flex-direction: column;
    gap: 0.1rem;
}

.ks-landing-stat strong {
    font-size: 1.5rem;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.02em;
}

.ks-landing-stat span {
    font-size: 0.84rem;
    color: #CBD5E1;
    font-weight: 500;
}

/* ── Skjema ── */
.ks-form-panel-head {
    padding: 0.35rem 0.85rem 0.85rem 0.85rem;
}

.ks-form-panel-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: var(--ks-text);
    letter-spacing: -0.02em;
    margin-bottom: 0.25rem;
}

.ks-form-panel-sub {
    font-size: 0.92rem;
    color: var(--ks-muted);
    line-height: 1.55;
}

.ks-form-section {
    background: var(--ks-panel);
    border: 1px solid var(--ks-border);
    border-radius: 14px;
    padding: 0.85rem 1rem;
    margin: 0.35rem 0.85rem 0.65rem 0.85rem;
}

.ks-form-section-head {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
}

.ks-step-icon {
    width: 2rem;
    height: 2rem;
    border-radius: 10px;
    background: linear-gradient(135deg, #1D4ED8, #38BDF8);
    color: #fff;
    font-size: 0.95rem;
    font-weight: 800;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex: 0 0 auto;
    box-shadow: 0 4px 12px rgba(29, 78, 216, 0.25);
}

.ks-form-section-copy {
    flex: 1;
    min-width: 0;
}

.ks-form-section-title {
    font-size: 1rem;
    font-weight: 700;
    color: var(--ks-text);
    margin-bottom: 0.15rem;
    line-height: 1.35;
}

.ks-form-section-sub {
    font-size: 0.9rem;
    color: var(--ks-muted);
    margin-bottom: 0;
    line-height: 1.55;
}

.ks-form-pill {
    display: inline-flex;
    align-items: center;
    padding: 0.12rem 0.55rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
    vertical-align: middle;
    margin-left: 0.35rem;
}

.ks-form-pill-optional {
    background: #ECFDF5;
    color: #047857;
    border: 1px solid #A7F3D0;
}

.ks-form-pill-required {
    background: #EFF6FF;
    color: #1D4ED8;
    border: 1px solid #BFDBFE;
}

.ks-field-hint {
    font-size: 0.875rem;
    color: var(--ks-muted);
    margin: 0 0.85rem 0.35rem 0.85rem;
    line-height: 1.5;
}

.ks-pick-banner {
    margin: 0.35rem 0.85rem 0.5rem 0.85rem;
    padding: 0.65rem 0.85rem;
    border-radius: 10px;
    font-size: 0.9rem;
    line-height: 1.45;
    border: 1px solid transparent;
}

.ks-pick-banner strong {
    display: block;
    font-weight: 700;
    color: var(--ks-text);
    margin-bottom: 0.1rem;
}

.ks-pick-banner span {
    color: var(--ks-muted);
    font-size: 0.875rem;
}

.ks-pick-banner-ok {
    background: #ECFDF5;
    border-color: #A7F3D0;
}

.ks-pick-banner-warn {
    background: #FFFBEB;
    border-color: #FDE68A;
    color: #92400E;
}

.ks-form-footer-note {
    margin: 0.5rem 0.85rem 0.25rem 0.85rem;
    padding: 0.75rem 0.9rem;
    background: #F1F5F9;
    border-radius: 10px;
    font-size: 0.9rem;
    color: var(--ks-text-soft);
    line-height: 1.55;
    border: 1px solid var(--ks-border);
}

.ks-form-footer-note strong {
    color: var(--ks-text);
}

.ks-landing-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.5rem;
}

.ks-brand-logo,
.ks-brand-fallback {
    width: 52px;
    height: 52px;
    border-radius: 14px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(148,163,184,0.25);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex: 0 0 auto;
}

.ks-brand-logo {
    object-fit: contain;
    padding: 6px;
}

.ks-brand-fallback {
    font-size: 0.9rem;
    font-weight: 900;
    color: #E2E8F0;
    letter-spacing: -0.02em;
}

.ks-brand-name {
    font-size: 1rem;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.02em;
    margin-bottom: 0.12rem;
}

.ks-landing-section {
    margin-bottom: 1.5rem;
}

.ks-landing-section-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--ks-text);
    margin-bottom: 0.35rem;
}

.ks-landing-section-sub {
    font-size: 0.82rem;
    color: var(--ks-muted);
    margin-bottom: 0.75rem;
}

.ks-feature-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
}

.ks-feature-card {
    background: var(--ks-surface);
    border: 1px solid var(--ks-border);
    border-radius: 12px;
    padding: 1.1rem 1.15rem;
    transition: box-shadow 0.15s, border-color 0.15s;
}

.ks-feature-card:hover {
    border-color: #BFDBFE;
    box-shadow: 0 4px 16px rgba(37,99,235,0.08);
}

.ks-feature-icon {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}

.ks-feature-title {
    font-size: 0.88rem;
    font-weight: 700;
    color: var(--ks-text);
    margin-bottom: 0.35rem;
}

.ks-feature-desc {
    font-size: 0.86rem;
    color: var(--ks-muted);
    line-height: 1.6;
}

.ks-steps {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    background: var(--ks-surface);
    border: 1px solid var(--ks-border);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
}

.ks-step {
    flex: 1;
    text-align: center;
}

.ks-step-num {
    width: 2rem;
    height: 2rem;
    background: linear-gradient(135deg, #2563EB, #1D4ED8);
    color: #fff;
    border-radius: 50%;
    font-size: 0.85rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 0.5rem;
}

.ks-step-title {
    font-size: 0.88rem;
    font-weight: 700;
    color: var(--ks-text);
    margin-bottom: 0.25rem;
}

.ks-step-desc {
    font-size: 0.86rem;
    color: var(--ks-muted);
    line-height: 1.55;
}

.ks-step-arrow {
    color: #CBD5E1;
    font-size: 1.25rem;
    padding-top: 0.4rem;
    flex-shrink: 0;
}

.ks-example-card {
    background: var(--ks-surface);
    border: 1px solid var(--ks-border);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    margin-bottom: 0.4rem;
    transition: border-color 0.15s;
}

.ks-example-card:hover {
    border-color: #93C5FD;
}

.ks-example-icon {
    font-size: 1.75rem;
    margin-bottom: 0.35rem;
}

.ks-example-name {
    font-size: 0.88rem;
    font-weight: 700;
    color: var(--ks-text);
    margin-bottom: 0.15rem;
}

.ks-example-industry {
    font-size: 0.72rem;
    color: var(--ks-muted);
    margin-bottom: 0.35rem;
}

.ks-example-tag {
    display: inline-block;
    font-size: 0.65rem;
    font-weight: 600;
    color: #2563EB;
    background: #EFF6FF;
    border-radius: 999px;
    padding: 0.15rem 0.5rem;
}

.ks-preview-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.6rem;
}

.ks-preview-item {
    background: var(--ks-surface);
    border: 1px solid var(--ks-border);
    border-radius: 10px;
    padding: 0.85rem 1rem;
}

.ks-preview-highlight {
    border-color: #2563EB;
    background: linear-gradient(135deg, #EFF6FF 0%, #FFFFFF 100%);
    box-shadow: 0 2px 12px rgba(37,99,235,0.1);
}

.ks-preview-label {
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--ks-text);
    margin-bottom: 0.25rem;
}

.ks-preview-text {
    font-size: 0.84rem;
    color: var(--ks-muted);
    line-height: 1.55;
}

.ks-trust-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.4rem 0.6rem;
    padding: 0.75rem 1rem;
    background: #F8FAFC;
    border: 1px solid var(--ks-border);
    border-radius: 10px;
    font-size: 0.72rem;
    color: var(--ks-muted);
    margin-bottom: 0.5rem;
}

.ks-trust-pill {
    background: #FFFFFF;
    border: 1px solid var(--ks-border);
    border-radius: 999px;
    padding: 0.15rem 0.55rem;
    font-weight: 600;
    color: var(--ks-text);
    font-size: 0.68rem;
}

.ks-trust-note {
    color: #94A3B8;
    font-size: 0.68rem;
}

@media (max-width: 900px) {
    .ks-feature-grid { grid-template-columns: repeat(2, 1fr); }
    .ks-preview-grid { grid-template-columns: repeat(2, 1fr); }
    .ks-landing-headline { font-size: 1.65rem; }
    .ks-steps { flex-direction: column; }
    .ks-step-arrow { display: none; }
    .ks-landing-hero { padding: 1.5rem 1.15rem 1.15rem; }
    .ks-landing-lead { font-size: 0.95rem; }
    .ks-form-section { margin-left: 0.35rem; margin-right: 0.35rem; }
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #fff;
    border-right: 1px solid var(--ks-border);
}

section[data-testid="stSidebar"] .block-container {
    padding: 0.75rem 0.75rem;
}

section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div {
    gap: 0.25rem;
}

.ks-sidebar-brand {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--ks-text);
}

.ks-sidebar-section {
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--ks-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin: 0.6rem 0 0.25rem 0;
}

.ks-status-pill {
    display: inline-flex;
    padding: 0.3rem 0.5rem;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 600;
    width: 100%;
    box-sizing: border-box;
}

.ks-status-ok { background: #ECFDF5; color: #047857; }
.ks-status-warn { background: #FFFBEB; color: #B45309; }

.ks-footer {
    text-align: center;
    font-size: 0.68rem;
    color: var(--ks-muted);
    margin-top: 0.75rem;
    padding-top: 0.5rem;
    border-top: 1px solid var(--ks-border);
}

/* ── Streamlit overrides ── */
.stTabs [data-baseweb="tab-list"] { gap: 0.25rem; min-height: 2rem; }
.stTabs [data-baseweb="tab"] {
    font-size: 0.78rem;
    font-weight: 600;
    padding: 0.35rem 0.75rem;
    height: auto;
}

div[data-testid="stButton"] > button {
    font-size: 0.95rem;
    padding: 0.55rem 1rem;
    min-height: 2.65rem;
}

div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #1D4ED8 0%, #2563EB 55%, #0284C7 100%);
    border: none;
    font-weight: 700;
    border-radius: 12px;
    box-shadow: 0 8px 20px rgba(29, 78, 216, 0.28);
}

div[data-testid="stButton"] > button[kind="primary"]:hover {
    box-shadow: 0 10px 24px rgba(29, 78, 216, 0.34);
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    font-size: 0.95rem;
    padding: 0.55rem 0.75rem;
    min-height: 2.45rem;
    border-radius: 10px;
    border-color: var(--ks-border);
    color: var(--ks-text);
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: #60A5FA;
    box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.18);
}

div[data-testid="stExpander"] {
    border: 1px solid var(--ks-border);
    border-radius: 10px;
    margin: 0 0.85rem 0.35rem 0.85rem;
    background: #FAFCFF;
}

div[data-testid="stExpander"] details summary {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--ks-text-soft);
    padding: 0.45rem 0.65rem;
}

div[data-testid="stTextInput"],
div[data-testid="stSelectbox"],
div[data-testid="stTextArea"] {
    margin-left: 0.85rem;
    margin-right: 0.85rem;
}

[data-testid="stSidebar"] div[data-testid="stButton"] > button {
    font-size: 0.72rem;
    padding: 0.25rem 0.5rem;
    min-height: 1.8rem;
    text-align: left;
}
</style>
"""
