"""Central configuration for the notification router adapted for local Ollama."""

import os
from types import MappingProxyType
from pathlib import Path
from typing import Mapping

from dotenv import load_dotenv


# Carga de .env desde el root
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

# Configuración del endpoint de Ollama / OpenAI compatible
OLLAMA_BASE_URL: str = os.environ.get("OPENAI_BASE_URL", "http://sputnik.local:11434/v1")
OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "ollama")
ANTHROPIC_API_KEY: str | None = os.environ.get("ANTHROPIC_API_KEY")

# Modelos locales con Ollama
DECISION_MODEL_PRIMARY: str = os.environ.get("DECISION_MODEL", "gemma4:26b")
DECISION_MODEL_DEV: str = "gemma4:26b"
FALLBACK_CHAIN: list[str] = ["gemma4:26b"]

# Transcripción desactivada (se omiten mensajes de audio)
TRANSCRIBE_MODEL: str | None = None
# Juez de evaluación usando el mismo modelo local
JUDGE_MODEL: str = "gemma4:26b"

# --- Ajustes de rendimiento y ejecución local ---
# Tool loops stop after four iterations to bound cost and runaway behavior.
MAX_TOOL_ITERATIONS: int = 4
# Límite de tokens de salida adecuado para llamadas de decisión
MAX_OUTPUT_TOKENS: int = 4_096
DECISION_EFFORT: str = "medium"
MAX_INSPECT_IMAGE_CALLS: int = 2
MAX_EVIDENCE_IDS: int = 2
MAX_RETRY_ATTEMPTS: int = 4
RETRY_BASE_SECONDS: float = 1.0
RETRY_CAP_SECONDS: float = 20.0
# Timeout por fila (3 minutos)
PER_ROW_TIMEOUT_SECONDS: int = 180
# Concurrencia adaptada para servidor local (1 o 2 hilos recomendados)
MAX_CONCURRENCY: int = 2
CONCURRENCY_RAMP_START: int = 1
# Redimensionado de imágenes para vision
MAX_IMAGE_DIMENSION: int = 1024

# --- Calibración de confianza y penalizaciones (NO TOCAR) ---
CONF_FLOOR: float = 0.55
CONF_CEIL: float = 0.95
MEDIA_MISMATCH_CONFIDENCE_PENALTY: float = 0.05
FIRST_CONTACT_CONFIDENCE_PENALTY: float = 0.05
HARD_BLOCK_CONFIDENCE: float = 0.85

# --- Rutas de datos (NO TOCAR) ---
DATASET_DIR: Path = Path("dataset")
OUTPUT_PATH: Path = DATASET_DIR / "output.csv"
TRACE_DIR: Path = Path("traces")
CACHE_DIR: Path = Path(".cache")

# --- Scoring y pesos de precedentes históricos (NO TOCAR) ---
RECENCY_HALF_LIFE_DAYS: float = 30.0
EVIDENCE_TOP_K: int = 6
EVIDENCE_MIN_SCORE: float = 0.12
W_SAME_PEER: float = 0.35
W_LEXICAL: float = 0.25
W_SAME_GROUP: float = 0.15
W_EVENT: float = 0.15
W_RECENCY: float = 0.10

EVENT_RELEVANCE: Mapping[str, float] = MappingProxyType(
    {
        "reported": 1.0,
        "muted_after": 0.9,
        "replied": 0.7,
        "dismissed": 0.6,
        "opened": 0.3,
    }
)

NEAR_DUPLICATE_TOP_K: int = 3
NEAR_DUPLICATE_MIN_JACCARD: float = 0.45
BURST_WINDOW_HOURS: int = 24
TRIGRAM_N: int = 3

# Precios por millón de tokens (0 para ejecución local)
MODEL_PRICE_PER_MTOK: Mapping[str, tuple[float, float]] = MappingProxyType(
    {
        "gemma4:26b": (0.00, 0.00),
        "claude-opus-5": (5.00, 25.00),
        "claude-sonnet-5": (3.00, 15.00),
    }
)
CACHE_READ_MULTIPLIER: float = 0.10
CACHE_WRITE_MULTIPLIER: float = 1.25

# --- Reglas de seguridad deterministas y reputación (NO TOCAR) ---
BRAND_MIN_AGE_DAYS: int = 365
BRAND_MIN_DOMAIN_AGE_DAYS: int = 180
BRAND_MAX_REPORTS: int = 29
DISMISS_MUTE_THRESHOLD: float = 0.5
MIN_PEER_HISTORY: int = 1