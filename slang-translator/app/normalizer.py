"""
Slang Normalizer - Converts informal/slang input to standard English.
Uses dictionary lookup + fuzzy matching + spelling normalization.
"""
import re
from typing import Optional, Tuple
from thefuzz import fuzz, process as fuzz_process
from app.slang_dictionary import SLANG_DB, SlangEntry, Region, Tone, lookup, get_all_entries


# Common spelling normalizations for repeated characters
REPEAT_PATTERN = re.compile(r'(.)\1{2,}')  # 3+ repeated chars → 2


def normalize_spelling(text: str) -> str:
    """Normalize repeated characters: 'kyaaa' → 'kyaa', 'yesss' → 'yess'."""
    return REPEAT_PATTERN.sub(r'\1\1', text)


def _preprocess(text: str) -> str:
    """Clean and normalize input text."""
    text = text.strip().lower()
    text = normalize_spelling(text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text


def exact_match(text: str) -> Optional[SlangEntry]:
    """Try exact dictionary lookup."""
    return lookup(text)


def phrase_match(text: str) -> list:
    """Find all slang phrases present in the text, longest first."""
    found = []
    # Sort keys by length (longest first) for greedy matching
    sorted_keys = sorted(SLANG_DB.keys(), key=len, reverse=True)
    remaining = text.lower()

    for key in sorted_keys:
        if key in remaining:
            entry = SLANG_DB[key]
            found.append((key, entry))
            remaining = remaining.replace(key, '', 1)

    return found


def fuzzy_match(text: str, threshold: int = 75) -> Optional[Tuple[SlangEntry, int]]:
    """Fuzzy match against slang dictionary."""
    all_keys = list(SLANG_DB.keys())
    if not all_keys:
        return None

    result = fuzz_process.extractOne(text, all_keys, scorer=fuzz.ratio)
    if result and result[1] >= threshold:
        matched_key = result[0]
        score = result[1]
        return SLANG_DB[matched_key], score

    return None


def normalize(text: str) -> dict:
    """
    Main normalization pipeline.
    Returns dict with normalized text and metadata.
    """
    original = text
    processed = _preprocess(text)

    # Step 1: Try exact match on full text
    entry = exact_match(processed)
    if entry:
        return {
            "original": original,
            "normalized": entry.meaning,
            "method": "exact_match",
            "confidence": 1.0,
            "tone": entry.tone.value,
            "region": entry.region.value,
            "slang_detected": entry.slang,
        }

    # Step 2: Try phrase matching (find slang within longer text)
    phrases = phrase_match(processed)
    if phrases:
        result_text = processed
        detected = []
        tones = []
        regions = []

        for key, entry in phrases:
            result_text = result_text.replace(key, entry.meaning, 1)
            detected.append(key)
            tones.append(entry.tone.value)
            regions.append(entry.region.value)

        # Clean up result
        result_text = re.sub(r'\s+', ' ', result_text).strip()

        return {
            "original": original,
            "normalized": result_text,
            "method": "phrase_match",
            "confidence": 0.85,
            "tone": tones[0] if tones else "neutral",
            "region": regions[0] if regions else "general",
            "slang_detected": ", ".join(detected),
        }

    # Step 3: Try fuzzy matching on individual words/phrases
    fuzzy = fuzzy_match(processed)
    if fuzzy:
        entry, score = fuzzy
        return {
            "original": original,
            "normalized": entry.meaning,
            "method": "fuzzy_match",
            "confidence": score / 100.0,
            "tone": entry.tone.value,
            "region": entry.region.value,
            "slang_detected": entry.slang,
        }

    # Step 4: No slang detected - return as-is
    return {
        "original": original,
        "normalized": processed,
        "method": "passthrough",
        "confidence": 0.5,
        "tone": "neutral",
        "region": "unknown",
        "slang_detected": None,
    }
