import os
from pathlib import Path
from urllib.parse import quote_plus

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Snowflake connection ──────────────────────────────────────────────────────
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "UATAI AUTOMATION HOSPITAL")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "DBO")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "AI AUTOMATION HOSPITAL_WH")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE", "SYSADMIN")

def _build_database_url() -> str:
    if SNOWFLAKE_ACCOUNT and SNOWFLAKE_USER and SNOWFLAKE_PASSWORD:
        pwd = quote_plus(SNOWFLAKE_PASSWORD)
        return (
            f"snowflake://{SNOWFLAKE_USER}:{pwd}@{SNOWFLAKE_ACCOUNT}"
            f"/{SNOWFLAKE_DATABASE}/{SNOWFLAKE_SCHEMA}"
            f"?warehouse={SNOWFLAKE_WAREHOUSE}&role={SNOWFLAKE_ROLE}"
        )
    return os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'ai_automation_hospital.db'}")

DATABASE_URL = _build_database_url()

IS_SNOWFLAKE = DATABASE_URL.startswith("snowflake://")

# ── Cortex AI ─────────────────────────────────────────────────────────────────
CORTEX_MODEL = os.getenv("CORTEX_MODEL", "llama3.1-8b")

# ── Business constants ────────────────────────────────────────────────────────
SPECIAL_HOSPITAL_DISPOSABLE = 99
SPECIAL_HOSPITAL_SPARE = 1001

MAX_CURTAINS_PER_BAG = 15
IN_STORAGE_HOLD_HOURS = 24

CURTAIN_PACKABLE_STATUSES = {"curtain_setup", "clean"}
CURTAIN_PACKABLE_STATUS_IDS: set[int] = set()
for _id in os.getenv("CURTAIN_PACKABLE_STATUS_IDS", "").split(","):
    _id = _id.strip()
    if _id.isdigit():
        CURTAIN_PACKABLE_STATUS_IDS.add(int(_id))

HISTORY_WINDOW_SIZE = 50

REDIS_URL = os.getenv("REDIS_URL", None)
CACHE_DEFAULT_TTL = int(os.getenv("CACHE_TTL", "300"))
