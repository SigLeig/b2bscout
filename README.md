# B2B Scout

AI-drevet B2B salgsintelligens for Norge — Brreg, regnskap, nyheter og salgsbrief.

![B2B Scout logo](assets/logo.png)

## Funksjoner

- **Brreg i sanntid** — org.form, bransje, ansatte, roller og risikoflag
- **Regnskap** — omsetning og driftsresultat fra Regnskapsregisteret
- **Nyheter** — Google News RSS (NewsAPI som valgfritt tillegg)
- **AI-analyse** — salgsbrief via Groq, xAI (Grok) eller OpenRouter
- **Ditt selskap + tilbud** — valgfri selgerkontekst for bedre produktmatch

## Kom i gang

### 1. Klon repoet

```bash
git clone https://github.com/SigLeig/b2bscout.git
cd b2bscout
```

### 2. Opprett virtuelt miljø

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Installer avhengigheter

```bash
pip install -r requirements.txt
```

### 4. Konfigurer miljøvariabler

Kopier malen (filen `.env.example` ligger i repo-roten):

```bash
copy .env.example .env   # Windows
# cp .env.example .env  # macOS / Linux
```

Hvis `.env.example` mangler etter clone, hent den fra GitHub eller lag `.env` manuelt med variablene under.

Rediger `.env` og legg inn minst én AI-nøkkel:

| Variabel | Beskrivelse |
|----------|-------------|
| `PROVIDER` | `groq`, `grok` eller `openrouter` |
| `GROQ_API_KEY` | [Groq Console](https://console.groq.com/keys) |
| `XAI_API_KEY` | [xAI Console](https://console.x.ai/) |
| `OPENROUTER_API_KEY` | [OpenRouter](https://openrouter.ai/keys) |
| `NEWS_API_KEY` | Valgfritt — [NewsAPI](https://newsapi.org/register) |

### 5. Kjør appen

```bash
python -m streamlit run app.py
```

Appen åpnes på [http://localhost:8501](http://localhost:8501).

## Bruk

1. **Ditt selskap** (valgfritt) — søk firmanavn eller skriv org.nr
2. **Hva selger du?** (valgfritt) — kort produktbeskrivelse
3. **Kunden** (påkrevd) — prospektet du vil analysere
4. Trykk **Analyser**

## Prosjektstruktur

```
b2bscout/
├── app.py              # Streamlit-app
├── config.py           # Miljøvariabler
├── assets/logo.png     # Logo
├── services/           # Brreg, regnskap, nyheter, AI
├── ui/                 # Komponenter og styling
└── utils/              # Formatering og org.nr-validering
```

## Datakilder

- [Brønnøysundregistrene](https://data.brreg.no/) (NLOD)
- [Regnskapsregisteret](https://data.brreg.no/regnskapsregisteret/)
- Google News RSS / NewsAPI
- Groq / xAI / OpenRouter

AI-generert innhold bør verifiseres før bruk i salg.

## Lisens

MIT — se [LICENSE](LICENSE).
