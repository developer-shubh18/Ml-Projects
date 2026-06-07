"""
Translation module using deep-translator (Google Translate wrapper).
"""
from deep_translator import GoogleTranslator

POPULAR_LANGUAGES = {
    "hi": "Hindi", "es": "Spanish", "fr": "French", "de": "German",
    "ja": "Japanese", "ko": "Korean", "zh-CN": "Chinese (Simplified)",
    "ar": "Arabic", "pt": "Portuguese", "ru": "Russian", "it": "Italian",
    "nl": "Dutch", "tr": "Turkish", "vi": "Vietnamese", "th": "Thai",
    "bn": "Bengali", "ta": "Tamil", "te": "Telugu", "mr": "Marathi",
    "ur": "Urdu", "pa": "Punjabi", "gu": "Gujarati", "ml": "Malayalam",
    "kn": "Kannada", "sw": "Swahili", "pl": "Polish", "uk": "Ukrainian",
    "id": "Indonesian", "ms": "Malay", "fil": "Filipino",
}

ALL_LANGUAGES = {}
try:
    ALL_LANGUAGES = GoogleTranslator().get_supported_languages(as_dict=True)
except Exception:
    ALL_LANGUAGES = {v: k for k, v in POPULAR_LANGUAGES.items()}


def get_all_languages() -> dict:
    return ALL_LANGUAGES

def get_popular_languages() -> dict:
    return POPULAR_LANGUAGES


def translate_text(text: str, target_lang: str, source_lang: str = "en") -> dict:
    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        result = translator.translate(text)
        return {
            "success": True,
            "original": text,
            "translated": result,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "target_lang_name": POPULAR_LANGUAGES.get(target_lang, target_lang),
        }
    except Exception as e:
        return {
            "success": False,
            "original": text,
            "translated": None,
            "error": str(e),
            "source_lang": source_lang,
            "target_lang": target_lang,
        }


def detect_language(text: str) -> dict:
    try:
        from langdetect import detect, detect_langs
        lang = detect(text)
        return {
            "language": lang,
            "language_name": POPULAR_LANGUAGES.get(lang, lang),
            "confidence": 0.9,
        }
    except Exception as e:
        return {"language": "unknown", "language_name": "Unknown", "confidence": 0, "error": str(e)}
