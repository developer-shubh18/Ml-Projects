"""
Slang & Dialect Translation System - FastAPI Application
Main API server with endpoints for normalization, translation, and the full pipeline.
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import os

from app.normalizer import normalize
from app.translator import (
    translate_text,
    detect_language,
    get_popular_languages,
    get_all_languages,
)
from app.slang_dictionary import (
    get_all_entries,
    get_entries_by_region,
    get_stats,
    Region,
)

# ─── App Setup ──────────────────────────────────────────────────────────

app = FastAPI(
    title="Slang & Dialect Translation System",
    description="Converts local slang → meaningful English → other languages",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# ─── Request / Response Models ──────────────────────────────────────────

class NormalizeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000, description="Slang text to normalize")

class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    target_lang: str = Field(..., min_length=2, max_length=10)
    source_lang: str = Field(default="en")

class PipelineRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000, description="Slang input")
    target_lang: str = Field(..., min_length=2, max_length=10, description="Target language code")

class BatchPipelineRequest(BaseModel):
    texts: List[str] = Field(..., max_length=20)
    target_lang: str = Field(..., min_length=2, max_length=10)


# ─── UI Route ───────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    """Serve the main UI."""
    html_path = os.path.join(STATIC_DIR, "index.html")
    with open(html_path, "r") as f:
        return HTMLResponse(content=f.read())


# ─── API Endpoints ──────────────────────────────────────────────────────

@app.post("/api/normalize")
async def api_normalize(req: NormalizeRequest):
    """Normalize slang to standard English."""
    result = normalize(req.text)
    return {"status": "success", "data": result}


@app.post("/api/translate")
async def api_translate(req: TranslateRequest):
    """Translate text to target language."""
    result = translate_text(req.text, req.target_lang, req.source_lang)
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error", "Translation failed"))
    return {"status": "success", "data": result}


@app.post("/api/pipeline")
async def api_pipeline(req: PipelineRequest):
    """Full pipeline: slang → English → target language."""
    # Step 1: Normalize
    norm_result = normalize(req.text)

    # Step 2: Translate normalized text
    trans_result = translate_text(norm_result["normalized"], req.target_lang)

    return {
        "status": "success",
        "data": {
            "original_input": req.text,
            "normalization": norm_result,
            "translation": trans_result,
            "pipeline_summary": {
                "input": req.text,
                "normalized_english": norm_result["normalized"],
                "final_translation": trans_result.get("translated", ""),
                "target_language": req.target_lang,
                "confidence": norm_result["confidence"],
                "tone_detected": norm_result["tone"],
                "region_detected": norm_result["region"],
            }
        }
    }


@app.post("/api/pipeline/batch")
async def api_pipeline_batch(req: BatchPipelineRequest):
    """Process multiple texts through the pipeline."""
    results = []
    for text in req.texts:
        norm = normalize(text)
        trans = translate_text(norm["normalized"], req.target_lang)
        results.append({
            "input": text,
            "normalized": norm["normalized"],
            "translated": trans.get("translated", ""),
            "confidence": norm["confidence"],
            "tone": norm["tone"],
        })
    return {"status": "success", "data": results}


@app.post("/api/detect-language")
async def api_detect_language(req: NormalizeRequest):
    """Detect the language of input text."""
    result = detect_language(req.text)
    return {"status": "success", "data": result}


@app.get("/api/languages")
async def api_languages():
    """Get list of supported languages."""
    return {
        "status": "success",
        "data": {
            "popular": get_popular_languages(),
            "all": get_all_languages(),
        }
    }


@app.get("/api/dictionary")
async def api_dictionary(region: Optional[str] = None):
    """Browse the slang dictionary."""
    if region:
        try:
            r = Region(region.lower())
            entries = get_entries_by_region(r)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid region: {region}")
    else:
        entries = get_all_entries()

    return {
        "status": "success",
        "data": [
            {
                "slang": e.slang,
                "meaning": e.meaning,
                "region": e.region.value,
                "tone": e.tone.value,
            }
            for e in entries
        ],
        "count": len(entries),
    }


@app.get("/api/stats")
async def api_stats():
    """Get system statistics."""
    stats = get_stats()
    return {"status": "success", "data": stats}


# ─── Health Check ───────────────────────────────────────────────────────

@app.get("/api/health")
async def health():
    return {"status": "healthy", "version": "1.0.0"}
