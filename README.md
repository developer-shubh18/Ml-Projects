# Ml-Projects

A collection of ML and NLP projects.

---

## 🌐 Slang & Dialect Translation System

A FastAPI-based web app that converts informal slang into standard English and then translates it into any target language.

### How it works

```
Slang Input → Normalize to English → Translate to Target Language
```

The normalizer uses a 3-step pipeline:
1. **Exact match** — looks up the slang directly in the dictionary
2. **Phrase match** — finds slang phrases embedded in longer text
3. **Fuzzy match** — handles typos and near-matches using `thefuzz`

### Supported Slang Regions

| Region | Examples |
|--------|---------|
| 🇮🇳 India / Hinglish | `bhai`, `yaar`, `jugaad`, `bawal`, `jhakaas` |
| 🇺🇸 US / Gen-Z | `no cap`, `bussin`, `rizz`, `slay`, `mid` |
| 🇬🇧 UK | `innit`, `mandem`, `peng`, `wagwan`, `gutted` |
| 🇦🇺 Australia | `arvo`, `brekkie`, `stoked`, `heaps` |
| 🌐 Internet | `lmao`, `ngl`, `fr`, `delulu`, `copium` |

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/normalize` | Normalize slang to standard English |
| `POST` | `/api/translate` | Translate text to a target language |
| `POST` | `/api/pipeline` | Full pipeline: slang → English → target language |
| `POST` | `/api/pipeline/batch` | Batch process multiple texts |
| `POST` | `/api/detect-language` | Detect language of input text |
| `GET` | `/api/languages` | List all supported languages |
| `GET` | `/api/dictionary` | Browse the slang dictionary (filter by region) |
| `GET` | `/api/stats` | Get dictionary statistics |
| `GET` | `/api/health` | Health check |

### Tech Stack

- **FastAPI** — API framework
- **deep-translator** — Google Translate wrapper
- **langdetect** — Language detection
- **thefuzz** — Fuzzy string matching
- **Jinja2 + aiofiles** — Static file serving

### Project Structure

```
slang-translator/
├── app/
│   ├── main.py              # FastAPI app and route definitions
│   ├── normalizer.py        # Slang normalization pipeline
│   ├── translator.py        # Translation and language detection
│   └── slang_dictionary.py  # Slang DB with region and tone metadata
├── static/
│   ├── index.html
│   ├── app.js
│   └── styles.css
└── requirements.txt
```

### Setup & Run

```bash
cd slang-translator
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open `http://localhost:8000` in your browser.
