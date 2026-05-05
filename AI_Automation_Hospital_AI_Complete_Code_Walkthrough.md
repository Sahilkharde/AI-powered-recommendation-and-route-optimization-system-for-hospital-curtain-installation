# AI Automation Hospital AI Agent — Complete Code Walkthrough

## Document Version: 1.0 | Date: April 13, 2026

---

## Table of Contents

1. [Project Architecture Overview](#1-project-architecture-overview)
2. [File: .env.example — Environment Variable Template](#2-file-envexample--environment-variable-template)
3. [File: requirements.txt — Python Dependencies](#3-file-requirementstxt--python-dependencies)
4. [File: .gitignore — Git Ignore Rules](#4-file-gitignore--git-ignore-rules)
5. [File: Dockerfile — Container Build](#5-file-dockerfile--container-build)
6. [File: app/config.py — Central Configuration](#6-file-appconfigpy--central-configuration)
7. [File: app/database.py — Database Engine and Sessions](#7-file-appdatabasepy--database-engine-and-sessions)
8. [File: app/models.py — All Database Tables (ORM Models)](#8-file-appmodelspy--all-database-tables-orm-models)
9. [File: app/schemas.py — API Request/Response Shapes](#9-file-appschemaspy--api-requestresponse-shapes)
10. [File: app/cache.py — Caching Layer](#10-file-appcachepy--caching-layer)
11. [File: app/seed.py — Sample Data Generator](#11-file-appseedpy--sample-data-generator)
12. [File: app/engine/rules.py — Business Rules (R1-R12)](#12-file-appenginerulesspy--business-rules-r1-r12)
13. [File: app/engine/scoring.py — Weighted Scoring Algorithm](#13-file-appenginescoringpy--weighted-scoring-algorithm)
14. [File: app/engine/recommender.py — Curtain to Track Recommendation Engine](#14-file-appenginerecommenderpy--curtain-to-track-recommendation-engine)
15. [File: app/engine/match.py — Track to Curtain Matching Engine](#15-file-appenginematchpy--track-to-curtain-matching-engine)
16. [File: app/engine/route.py — Installer Route Optimizer](#16-file-appengineroutepy--installer-route-optimizer)
17. [File: app/agents/installation_agent.py — Cortex AI Agent](#17-file-appagentsinstallation_agentpy--cortex-ai-agent)
18. [File: app/api/routes.py — All HTTP Endpoints](#18-file-appapiroutespy--all-http-endpoints)
19. [File: app/main.py — Application Entry Point](#19-file-appmainpy--application-entry-point)
20. [File: app/static/index.html — Mobile-First Web UI](#20-file-appstaticindexhtml--mobile-first-web-ui)
21. [File: demo.py — CLI Test Script](#21-file-demopy--cli-test-script)
22. [Test Files Overview](#22-test-files-overview)
23. [Snowflake Cortex AI — Plan and Pricing](#23-snowflake-cortex-ai--plan-and-pricing)
24. [Data Storage in Snowflake](#24-data-storage-in-snowflake)
25. [Data Required for AI Features](#25-data-required-for-ai-features)

---

## 1. Project Architecture Overview

```
ai automation hospital-ai/
├── .env.example          — Environment variable template
├── .gitignore            — Git ignore rules
├── requirements.txt      — Python dependencies
├── Dockerfile            — Container build instructions
├── demo.py               — CLI test script
├── app/
│   ├── main.py           — FastAPI app entry point
│   ├── config.py         — All configuration and business constants
│   ├── database.py       — DB engine, sessions, Snowpark session
│   ├── models.py         — SQLAlchemy ORM models (mirrors SQL Server)
│   ├── schemas.py        — Pydantic request/response shapes
│   ├── cache.py          — In-memory TTL cache + optional Redis
│   ├── seed.py           — Populates SQLite with sample data
│   ├── api/
│   │   └── routes.py     — All HTTP endpoints
│   ├── engine/
│   │   ├── rules.py      — Business rules R1-R12
│   │   ├── scoring.py    — Weighted scoring algorithm
│   │   ├── recommender.py— Curtain to Track recommendation engine
│   │   ├── match.py      — Track to Curtain matching engine
│   │   └── route.py      — Installer route optimizer
│   ├── agents/
│   │   └── installation_agent.py — Cortex AI agent (LLM explanation)
│   └── static/
│       └── index.html    — Mobile-first web UI
└── tests/
    ├── test_rules.py
    ├── test_scoring.py
    ├── test_recommender.py
    ├── test_match.py
    ├── test_route.py
    ├── test_api_endpoints.py
    └── test_cache.py
```

### How the System Works (Data Flow)

1. An installer scans a **curtain barcode** using the mobile web UI or the API.
2. The system looks up the curtain in the database (type, style, hospital, dimensions).
3. The **rules engine** filters out ineligible tracks (wrong hospital, wrong type, at capacity).
4. The **scoring engine** scores every remaining track on 6 signals: history, size, type, style, recency, capacity.
5. Results are ranked and returned to the installer as a list of "Install HERE" recommendations.
6. Optionally, **Snowflake Cortex AI** generates a plain-English explanation for the installer.

The reverse flow also works: scan a **track barcode** to find matching curtains.

A third feature optimizes the **installer's daily route** across hospitals/buildings/floors.

---

## 2. File: .env.example — Environment Variable Template

**Purpose:** Documents every configurable setting for the application. This file is committed to git as a template. The actual `.env` file with real values is never committed (it is in `.gitignore`).

### Snowflake Connection (Lines 4-17)

```
SNOWFLAKE_ACCOUNT=your_account.us-east-1
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_DATABASE=UATAI AUTOMATION HOSPITAL
SNOWFLAKE_SCHEMA=DBO
SNOWFLAKE_WAREHOUSE=AI AUTOMATION HOSPITAL_WH
SNOWFLAKE_ROLE=SYSADMIN
```

**Logic:** If all three required variables (`SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`) are set, the app connects to Snowflake as its database instead of SQLite. The defaults (`UATAI AUTOMATION HOSPITAL`, `DBO`, `AI AUTOMATION HOSPITAL_WH`, `SYSADMIN`) match the naming conventions in the real AI Automation Hospital SQL Server production database. This ensures a seamless transition from SQL Server to Snowflake.

### Cortex AI Model (Lines 19-26)

```
CORTEX_MODEL=llama3.1-8b
```

**Logic:** Picks which Large Language Model to use when generating installer explanations via Snowflake Cortex AI. The default `llama3.1-8b` is the cheapest and fastest option, ideal for trial accounts. Other options include `llama3.1-70b` (better quality, higher cost), `mistral-large` (mid-tier), and `claude-3-5-sonnet` (highest quality, highest cost). This setting is only used when connected to Snowflake.

### Curtain Packable Statuses (Lines 28-30)

```
CURTAIN_PACKABLE_STATUS_IDS=1,2
```

**Logic:** Comma-separated status ID values that mean "this curtain is ready to be packed and installed." Only curtains with these statuses should appear in recommendations. Status ID 1 = "Curtain Setup", Status ID 2 = "Clean". This maps to the `Curt_Status` lookup table in the database.

### Redis Cache (Lines 32-34)

```
REDIS_URL=redis://localhost:6379/0
```

**Logic:** Optional Redis connection URL. If set and the `redis` Python package is installed, the app uses Redis for caching instead of the default in-memory cache. Redis is better for production because the cache survives server restarts and can be shared across multiple app instances.

### Cache TTL (Lines 36-37)

```
CACHE_TTL=300
```

**Logic:** How many seconds cached results stay valid. Default is 300 seconds (5 minutes). After this time, cached results are discarded and fresh results are computed from the database. A shorter TTL means more up-to-date results but more database queries; a longer TTL means faster responses but potentially stale data.

---

## 3. File: requirements.txt — Python Dependencies

```
fastapi>=0.115.0
uvicorn>=0.34.0
sqlalchemy>=2.0.0
pydantic>=2.0.0
python-dateutil>=2.9.0
python-dotenv>=1.0.0
pytest>=8.0.0
snowflake-sqlalchemy>=1.7.0
snowflake-ml-python>=1.7.0
```

### Why Each Dependency is Needed

| Package | Purpose |
|---------|---------|
| `fastapi` | The web framework. Handles HTTP requests, validates input, auto-generates interactive API documentation at `/docs`. |
| `uvicorn` | The ASGI server that actually runs the FastAPI application. Handles networking, concurrency, and HTTP protocol. |
| `sqlalchemy` | Object-Relational Mapper (ORM). Lets us write Python classes instead of raw SQL queries. The same code works with SQLite, SQL Server, and Snowflake. |
| `pydantic` | Data validation library. Every API request body and response body is validated against a Pydantic model. Invalid data is automatically rejected with clear error messages. |
| `python-dateutil` | Date parsing helpers. Used for parsing route dates in the installer route optimizer. |
| `python-dotenv` | Reads the `.env` file and loads its contents into environment variables. This happens before any other code runs. |
| `pytest` | The test runner. Discovers and executes all test files in the `tests/` directory. |
| `snowflake-sqlalchemy` | SQLAlchemy dialect for Snowflake. This allows SQLAlchemy to generate Snowflake-compatible SQL and connect to Snowflake databases. The same ORM models work against both SQLite (for development) and Snowflake (for production). |
| `snowflake-ml-python` | Provides the `snowflake.cortex.complete()` function. This is the Python API for calling Snowflake Cortex AI's large language models to generate text. |

---

## 4. File: .gitignore — Git Ignore Rules

```
__pycache__/
*.pyc
*.pyo
*.db
.env
.venv/
venv/
*.egg-info/
dist/
build/
.pytest_cache/
```

**Logic:** Prevents the following from being committed to version control:

- `__pycache__/`, `*.pyc`, `*.pyo` — Compiled Python bytecode files. These are auto-generated and machine-specific.
- `*.db` — SQLite database files (like `ai_automation_hospital_ai.db`). These contain data and should not be in version control.
- `.env` — The real environment file containing Snowflake credentials, passwords, and API keys. This is a security measure.
- `.venv/`, `venv/` — Python virtual environments. These contain installed packages and are large.
- `*.egg-info/`, `dist/`, `build/` — Python packaging artifacts.
- `.pytest_cache/` — Test runner cache.

---

## 5. File: Dockerfile — Container Build

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ app/
RUN python -m app.seed
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Line-by-Line Logic

1. **`FROM python:3.12-slim`** — Uses the official Python 3.12 slim image as the base. "Slim" means it excludes development tools to keep the image small (approximately 150MB vs 1GB for the full image).

2. **`WORKDIR /app`** — Sets `/app` as the working directory inside the container. All subsequent commands run from this directory.

3. **`COPY requirements.txt .`** — Copies only the requirements file first. This is a Docker optimization: if the requirements don't change between builds, Docker reuses the cached layer from step 4.

4. **`RUN pip install --no-cache-dir -r requirements.txt`** — Installs all Python packages. `--no-cache-dir` prevents pip from saving downloaded packages, keeping the image smaller.

5. **`COPY app/ app/`** — Copies the application code into the container.

6. **`RUN python -m app.seed`** — Runs the seed script at build time. This creates the SQLite database with sample hospitals, buildings, rooms, tracks, curtains, and installation history so the application can be tested immediately.

7. **`EXPOSE 8000`** — Documents that the container listens on port 8000.

8. **`CMD [...]`** — Starts the Uvicorn server, binding to all network interfaces (`0.0.0.0`) on port 8000.

---

## 6. File: app/config.py — Central Configuration

### Imports (Lines 1-3)

```python
import os
from pathlib import Path
from urllib.parse import quote_plus
```

- `os` — Reads environment variables.
- `Path` — Cross-platform file path handling.
- `quote_plus` — URL-encodes the Snowflake password so special characters (like `@`, `#`, `&`) don't break the connection URL.

### BASE_DIR (Line 5)

```python
BASE_DIR = Path(__file__).resolve().parent.parent
```

**Logic:** Computes the project root directory. `__file__` is `app/config.py`, `.parent` goes to `app/`, `.parent` again goes to the project root. Used to locate the SQLite database file.

### Snowflake Connection Variables (Lines 8-14)

```python
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "UATAI AUTOMATION HOSPITAL")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "DBO")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "AI AUTOMATION HOSPITAL_WH")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE", "SYSADMIN")
```

**Logic:** Each variable reads from an environment variable. The first three have no default (they are None if not set — this is the signal to use SQLite instead). The remaining four have defaults matching the AI Automation Hospital production database naming.

### Database URL Builder (Lines 16-24)

```python
def _build_database_url() -> str:
    if SNOWFLAKE_ACCOUNT and SNOWFLAKE_USER and SNOWFLAKE_PASSWORD:
        pwd = quote_plus(SNOWFLAKE_PASSWORD)
        return (
            f"snowflake://{SNOWFLAKE_USER}:{pwd}@{SNOWFLAKE_ACCOUNT}"
            f"/{SNOWFLAKE_DATABASE}/{SNOWFLAKE_SCHEMA}"
            f"?warehouse={SNOWFLAKE_WAREHOUSE}&role={SNOWFLAKE_ROLE}"
        )
    return os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'ai_automation_hospital_ai.db'}")
```

**Logic:** This is the key decision function:

- **If all 3 Snowflake credentials are set:** Build a Snowflake connection URL in the format SQLAlchemy expects: `snowflake://user:password@account/database/schema?warehouse=...&role=...`. The password is URL-encoded for safety.
- **Otherwise:** Check for a custom `DATABASE_URL` environment variable. If that is also not set, default to a local SQLite file at `{project_root}/ai_automation_hospital_ai.db`.

This design means the exact same application code works in three environments:
1. Local development with SQLite (no configuration needed)
2. Custom database (set `DATABASE_URL`)
3. Snowflake production (set Snowflake credentials)

### IS_SNOWFLAKE Flag (Line 28)

```python
IS_SNOWFLAKE = DATABASE_URL.startswith("snowflake://")
```

**Logic:** A boolean flag used throughout the app to enable/disable Snowflake-specific features:
- Skip table creation on Snowflake (tables already exist)
- Enable Cortex AI calls (only work on Snowflake)
- Create Snowpark sessions for LLM calls

### Cortex AI Model (Line 31)

```python
CORTEX_MODEL = os.getenv("CORTEX_MODEL", "llama3.1-8b")
```

**Logic:** The LLM model name passed to `snowflake.cortex.complete()`. Defaults to `llama3.1-8b` — the cheapest model available.

### Business Constants (Lines 34-50)

```python
SPECIAL_HOSPITAL_DISPOSABLE = 99
SPECIAL_HOSPITAL_SPARE = 1001
MAX_CURTAINS_PER_BAG = 15
IN_STORAGE_HOLD_HOURS = 24
CURTAIN_PACKABLE_STATUSES = {"curtain_setup", "clean"}
CURTAIN_PACKABLE_STATUS_IDS: set[int] = set()
HISTORY_WINDOW_SIZE = 50
REDIS_URL = os.getenv("REDIS_URL", None)
CACHE_DEFAULT_TTL = int(os.getenv("CACHE_TTL", "300"))
```

**Logic for each constant:**

- **`SPECIAL_HOSPITAL_DISPOSABLE = 99`** — Hospital ID 99 is a virtual hospital that holds all disposable curtains. Disposable curtains can be installed at any real hospital. This is a AI Automation Hospital business convention.
- **`SPECIAL_HOSPITAL_SPARE = 1001`** — Hospital ID 1001 holds spare/backup curtains. Like disposables, spares can go to any hospital.
- **`MAX_CURTAINS_PER_BAG = 15`** — Business rule R4: a transport bag can hold a maximum of 15 curtains. This is enforced by the rules engine.
- **`IN_STORAGE_HOLD_HOURS = 24`** — Reserved for future use: how long curtains can be held in temporary storage before they must be processed.
- **`CURTAIN_PACKABLE_STATUSES`** — String-based set of status names that mean "ready to install."
- **`CURTAIN_PACKABLE_STATUS_IDS`** — Integer-based set parsed from the environment variable `CURTAIN_PACKABLE_STATUS_IDS`. The parsing loop (lines 42-45) splits the comma-separated string, strips whitespace, and converts each valid integer into the set.
- **`HISTORY_WINDOW_SIZE = 50`** — When querying installation history for scoring, limit to the top 50 most-used tracks. This prevents extremely old data from dominating recommendations.
- **`REDIS_URL`** — Optional Redis connection string.
- **`CACHE_DEFAULT_TTL`** — Cache time-to-live in seconds, parsed from environment variable.

---

## 7. File: app/database.py — Database Engine and Sessions

### Engine Setup (Lines 1-11)

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import DATABASE_URL, IS_SNOWFLAKE

connect_args: dict = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

**Logic:**

- **`create_engine(DATABASE_URL)`** — Creates a database connection pool. SQLAlchemy manages the pool automatically.
- **`check_same_thread=False`** — SQLite by default only allows the thread that created the connection to use it. FastAPI uses async workers on multiple threads, so this setting is required to prevent `ProgrammingError: SQLite objects created in a thread can only be used in that same thread`.
- **`SessionLocal`** — A factory that creates database sessions. `autocommit=False` means we must explicitly commit transactions. `autoflush=False` means SQL is not automatically sent to the database until we call `.flush()` or `.commit()`.

### Base Class (Lines 14-15)

```python
class Base(DeclarativeBase):
    pass
```

**Logic:** Every ORM model in `models.py` inherits from this class. It provides the `metadata` attribute that SQLAlchemy uses to track table definitions, and it provides the mapping between Python classes and database tables.

### get_db() Dependency (Lines 18-23)

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Logic:** A FastAPI dependency injection function. Every API endpoint that needs database access declares `db: Session = Depends(get_db)`. The `yield` pattern ensures:

1. A new session is created when the request starts.
2. The session is available to the endpoint function.
3. The session is **always** closed when the request finishes, even if an exception occurred.

This is the "session per request" pattern — each HTTP request gets its own isolated database session.

### init_db() (Lines 26-29)

```python
def init_db():
    if IS_SNOWFLAKE:
        return
    Base.metadata.create_all(bind=engine)
```

**Logic:** Creates all tables defined in `models.py` in the database. However, this is skipped when connected to Snowflake because:

1. The tables already exist in the Snowflake database (they were created by the AI Automation Hospital production system).
2. Snowflake's DDL syntax is different from SQLite, and auto-creation could cause issues.

### get_snowflake_session() (Lines 32-62)

```python
def get_snowflake_session():
    if not IS_SNOWFLAKE:
        return None
    try:
        from snowflake.snowpark import Session as SnowparkSession
        return SnowparkSession.builder.configs({
            "account": SNOWFLAKE_ACCOUNT,
            "user": SNOWFLAKE_USER,
            "password": SNOWFLAKE_PASSWORD,
            "database": SNOWFLAKE_DATABASE,
            "schema": SNOWFLAKE_SCHEMA,
            "warehouse": SNOWFLAKE_WAREHOUSE,
            "role": SNOWFLAKE_ROLE,
        }).create()
    except Exception:
        return None
```

**Logic:** Creates a Snowpark Session specifically for Cortex AI calls. This is separate from the SQLAlchemy engine because:

- SQLAlchemy handles regular SQL queries (SELECT, INSERT, etc.)
- Snowpark handles Snowflake-specific operations like calling Cortex `complete()`

The function:
1. Returns `None` immediately if not connected to Snowflake.
2. Lazy-imports `SnowparkSession` (so the snowflake package is only required when actually using Snowflake).
3. Creates a session with the same credentials as the SQLAlchemy connection.
4. Returns `None` on any exception (graceful degradation).

---

## 8. File: app/models.py — All Database Tables (ORM Models)

**Purpose:** Maps every table from the AI Automation Hospital SQL Server database (`UATAI Automation Hospital`) to Python classes using SQLAlchemy. Column names and table names match the production database exactly, including misspellings like `Deleiverd_by`, `CellingHeight`, and `GoormateID`. This is intentional — it ensures the ORM works against the real database without any column name translation.

### Understanding the ORM Pattern

Each class represents a database table. Each class attribute represents a column. For example:

```python
class Hospital(Base):
    __tablename__ = "Hospital"
    HID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Name: Mapped[str | None] = mapped_column(String(50), nullable=True)
```

This tells SQLAlchemy: "There is a table called `Hospital` with a column `HID` (integer, primary key, auto-incrementing) and a column `Name` (varchar(50), nullable)."

### Group 1: Lookup/Reference Tables (Lines 30-286)

These are small, rarely-changing tables used for dropdown menus and picklists in the AI Automation Hospital application:

| Model Class | Table Name | What It Stores | Key Fields |
|------------|------------|----------------|------------|
| `CurtType` | `Curt_Type` | Curtain types | Standard, Snap, Psyc |
| `CurtPatterns` | `Curt_Patterns` | Fabric patterns | Pattern descriptions, image URLs |
| `CurtWidth` | `Curt_Width` | Available curtain widths | 36", 48", 60", 72", 84", 96" |
| `CurtHeight` | `Curt_Height` | Available curtain heights | 72", 84", 96", 108" |
| `CurtGrommets` | `Curt_Grommets` | Grommet types | Standard, Snap |
| `CurtStyle` | `Curt_Style` | Curtain styles | Style descriptions |
| `CurtColor` | `Curt_Color` | Curtain colors | Color descriptions |
| `CurtStatus` | `Curt_Status` | Curtain lifecycle states | Curtain Setup, Clean, Soiled, Installed, Delivered |
| `UnitLookup` | `Units` | Hospital unit types | ICU, General Ward, Surgical, Emergency, Pediatrics, etc. |
| `LocationLookup` | `Location` | Location categories | Location names |
| `TrackType` | `TrackType` | Track shapes | Straight, L-Shape, U-Shape |
| `TrackLocation` | `TrackLocation` | Track positions within rooms | Position names |
| `MeshColor` | `Mesh_Color` | Mesh curtain colors | Color descriptions |
| `MeshSize` | `Mesh_Size` | Mesh curtain sizes | Size descriptions |
| `MeshType` | `Mesh_Type` | Mesh curtain types | Type descriptions |
| `HospRegion` | `Hosp_Regions` | Geographic regions | Region descriptions |
| `InstallerTypeLookup` | `Installertype` | Installer certifications | Type descriptions |
| `MaintenanceType` | `MaintenanceType` | Types of maintenance | Name, description |
| `ScheduleTerm` | `ScheduleTerm` | Schedule frequencies | Name, frequency in months/days |
| `PricingType` | `PricingType` | Pricing categories | Name, washing price flag |
| `BagLocationType` | `BagLocationType` | Bag storage types | Location type names |
| `WeekDays` | `WeekDays` | Days of the week | Names (Monday through Sunday) |
| `DropDownComments` | `DropDownComments` | Predefined comments | Comment text, status |
| `LocationStatus` | `LocationStatus` | Location states | Status text, dates |
| `AppVersion` | `AppVersion` | App versions | Version number, active flag |
| `CountryImages` | `CountryImages` | Country flag images | Country name, image path |
| `TblCountry` | `tblcountry` | Countries | Code, description, country code |
| `TblStateCountry` | `tblStateCountry` | States per country | State code, country code, name |

All lookup tables share a common pattern: an integer primary key, a name/description field, a `SortIndex` for display ordering, and an `Enabled` boolean flag.

### Group 2: Core Entity Tables (Lines 288-588)

#### Hospital (Line 293)

**Table:** `Hospital`
**Purpose:** Every hospital that AI Automation Hospital serves.

| Column | Type | Logic |
|--------|------|-------|
| `HID` | Integer PK | Hospital ID. Special values: 99 = disposable curtains storage, 1001 = spare curtains storage. |
| `Name` | String(50) | Hospital name (e.g., "Florida General Hospital"). |
| `Address`, `City`, `StateId`, `Zip`, `CountryCode` | Various | Physical address for GPS routing. |
| `Phone`, `Extension`, `Fax`, `Email` | Various | Contact info. |
| `EVS_Name`, `EVS_Phone`, `EVS_Extension`, `EVS_Email`, `EVS_Cell` | Various | Environmental Services contact (the hospital staff who coordinate curtain changes). |
| `contactPer_Name`, `contactPer_Phone`, etc. | Various | Additional contact person. |
| `AccountNumber` | Integer | Used as the prefix for track barcodes. E.g., account 1576 means tracks are labeled `1576-T0001`, `1576-T0002`, etc. |
| `VisitDay` | Integer | Preferred day of week for installer visits. |
| `Maintenance` | String(20) | Maintenance type preference. |
| `Latitude`, `Longitude` | String(50) | GPS coordinates for route optimization. |
| `RegionId` | Integer | Geographic region for grouping. |
| `IsManufecturingService` | Boolean | Whether this is a manufacturing facility. |
| `isTempStorage` | Boolean | Whether this hospital has temporary curtain storage areas. |
| `IsHospitalOwnedCurtains` | Boolean | Whether the hospital owns its own curtains (vs. AI Automation Hospital owned). |
| `HasAIAutomationHospitalSpares` | Boolean | Whether AI Automation Hospital provides spare curtains here. |
| `HasDisposable` | Boolean | Whether disposable curtains are used here. |
| `buildings` | Relationship | Links to all `HospBuilding` records for this hospital. |
| `curtains` | Relationship | Links to all `HospCurtain` records owned by this hospital. |

#### HospBuilding (Line 342)

**Table:** `Hosp_Building`
**Purpose:** Buildings within a hospital.

| Column | Type | Logic |
|--------|------|-------|
| `BID` | Integer PK | Building ID. |
| `HID` | ForeignKey → Hospital | Which hospital this building belongs to. |
| `Name` | String(50) | Building name (e.g., "Cancer Care Block", "West Wing"). |
| `TotalFloor` | Integer | Number of floors in this building. |
| `IsLocked` | Boolean | Whether the building is locked for changes (during active installations). |
| `hospital` | Relationship | Back-reference to the parent Hospital. |
| `units` | Relationship | Links to all `HospUnit` records in this building. |

#### HospUnit (Line 364)

**Table:** `Hosp_Unit`
**Purpose:** A unit/ward within a building (e.g., "ICU on Floor 2").

| Column | Type | Logic |
|--------|------|-------|
| `HUID` | Integer PK | Unit ID (Hospital Unit ID). |
| `BID` | ForeignKey → Hosp_Building | Which building this unit is in. |
| `UnitID` | ForeignKey → Units | References the lookup table for the unit type (ICU, General Ward, etc.). |
| `Floor` | Integer | Which floor of the building. Used in route sorting. |
| `Style` | Integer | The curtain style preferred for this unit. Used in scoring — style match between curtain and unit. |
| `CellingHeight` | String(15) | Ceiling height in feet. Affects which curtain heights are appropriate. |
| `SparesRequired` | Boolean | Whether this unit needs spare curtains. |
| `Schudule` | Integer | Maintenance schedule reference. |
| `unit_name` property | String | Resolves the display name from the `Units` lookup table. If no lookup exists, returns "Unit {HUID}". |
| `rooms` | Relationship | Links to all `HospBuildingRoom` records. |
| `tracks` | Relationship | Links to all `HospTrack` records. |

#### HospBuildingRoom (Line 409)

**Table:** `Hosp_Building_Rooms`
**Purpose:** Individual rooms within a unit.

| Column | Type | Logic |
|--------|------|-------|
| `RoomID` | Integer PK | Room ID. |
| `HUID` | ForeignKey → Hosp_Unit | Which unit this room is in. |
| `RoomNumber` | String(50) | Display name (e.g., "101", "Room 201"). |
| `tracks` | Relationship | Links to all tracks in this room. |

#### HospTrack (Line 429)

**Table:** `Hosp_Track`
**Purpose:** Curtain tracks — the physical hardware rails mounted on hospital ceilings. This is the **core entity** that the AI system recommends.

| Column | Type | Logic |
|--------|------|-------|
| `HospTrackId` | Integer PK | Track ID. |
| `HUID` | ForeignKey → Hosp_Unit | Which unit this track is in. |
| `RoomId` | ForeignKey → Hosp_Building_Rooms | Which room this track is in. |
| `TrackBarCode` | String(20) | The barcode label on the track (e.g., "1576-T0001"). This is what installers scan. |
| `TrackTypeID` | ForeignKey → TrackType | Shape: Straight, L-Shape, U-Shape. |
| `Length` | String(10) | Track length in inches. Stored as string (e.g., "72"). |
| `Height` | String(10) | Track height in inches. Stored as string (e.g., "84"). |
| `Curt_TypeId` | ForeignKey → Curt_Type | Expected curtain type for this track (Standard, Snap, Psyc). |
| `CurtainStyle` | Integer | Style preference. |
| `NumberOfCurtain` | Integer | Maximum regular curtains this track can hold. |
| `NumberOfSpares` | Integer | Additional capacity for spare curtains (above the regular limit). |
| `NumberOfDisposables` | Integer | Additional capacity for disposable curtains. |
| `Track_status` | Integer | Current status of the track. |
| `Due_Date` | DateTime | When the next service is due. |
| `length_value` property | Float | Parses the string `Length` to a float, stripping quote marks and whitespace. Returns None if parsing fails. |
| `height_value` property | Float | Same parsing for `Height`. |

#### HospCurtain (Line 484)

**Table:** `Hosp_Curtains`
**Purpose:** Individual curtains. This is what installers **scan** to get recommendations.

| Column | Type | Logic |
|--------|------|-------|
| `CID` | Integer PK | Curtain ID. |
| `HID` | ForeignKey → Hospital | Which hospital owns this curtain. Special values: 99 = disposable, 1001 = spare. |
| `CurtBarCode` | Integer (Unique) | The barcode on the curtain. This is the primary input to the AI system. |
| `Curt_TypeID` | ForeignKey → Curt_Type | Curtain type: Standard, Snap, or Psyc. |
| `UnitStyle` | Integer | The style this curtain is designed for. Compared against unit style during scoring. |
| `WidthId` | Integer | Width code. Used as an approximate numeric width value for size matching. |
| `HeightId` | Integer | Height code. |
| `PatternID` | Integer | Fabric pattern. |
| `GrommetID` | ForeignKey → Curt_Grommets | Grommet type. |
| `Mesh` | Boolean | Whether this is a mesh curtain. |
| `Weight` | Float | Physical weight of the curtain. |
| `IsManufecturing` | Boolean | Whether this is a manufacturing-stage curtain. |
| `NoofPannels` | Integer | Number of panels. |
| `SnapMesh` | Integer | Snap mesh count. |
| `SONumber` | String(50) | Sales order number. |
| `LotNumber` | String(50) | Manufacturing lot number. |
| `barcode_str` property | String | Converts the integer CurtBarCode to a string for display and API responses. |

### Group 3: Service/Operational Tables (Lines 592-764)

#### TrackCurtainService (Line 596)

**Table:** `Track_Curtain_Services`
**Purpose:** The most important table for AI recommendations. Every time a curtain is installed on a track, removed, cleaned, or serviced, a record is created here. This is the **installation history** that drives the scoring engine.

| Column | Type | Logic |
|--------|------|-------|
| `ID` | Integer PK | Service record ID. |
| `CurBarCode` | Integer | Which curtain was involved. |
| `TrackBarCode` | String(20) | Which track it was installed on. |
| `CurStatusID` | Integer | Status at time of service. |
| `Installed_By` | String(50) | The user ID of the installer. Used to determine which tracks an installer is responsible for (route optimization). |
| `Installed_Date` | DateTime | When the installation happened. Used for recency scoring. |
| `Date_Created` | DateTime | When the record was created. |
| `ServiceType` | String(20) | "Maintenance", "Installation", etc. |
| `CleanedAndR_Date` / `CleanedAndR_By` | DateTime / String | Cleaning records. |
| `Deleiverd_Date` / `Deleiverd_by` | DateTime / String | Delivery records (note: misspelling matches production DB). |
| `SoiledScanedDate` / `SoiledScanedBy` | DateTime / String | Soiled curtain scan records. |
| `IsRewash` / `RewashDate` / `Rewash_By` | Boolean / DateTime / String | Rewash tracking. |
| `IsRemesh` / `RemeshDate` / `remesh_By` | Boolean / DateTime / String | Remesh tracking. |

#### Visit (Line 627)

**Table:** `Visit`
**Purpose:** Represents a single visit by an installer to a hospital. Contains all visit metadata.

Key fields: `VisitDate`, `HID` (which hospital), `VisitedBy` (installer), `NoOfCurtains`, `serviceType`, `ClientSignature`, `StartTime`/`EndTime`, `NoOfBags`, `VisitType`, `IsTempSotrage`.

#### VisitDetail (Line 660)

**Table:** `VisitDetail`
**Purpose:** Each curtain-track pair processed during a visit. Composite primary key: `(VisitId, CurtBarCode)`.

### Group 4: User/Role Tables (Lines 768-832)

- **`AIAutomationHospitalUser`** — All system users (installers, admins, managers). Fields: USER_ID, names, email, phone, UserType, InstallerType, MobilePass.
- **`AIAutomationHospitalRoleGroup`** — Named role groups (e.g., "Admin", "Installer", "Manager").
- **`AIAutomationHospitalRoleGroupRole`** — Which permissions belong to each role group.
- **`AIAutomationHospitalRoleGroupUser`** — Which users belong to which role groups.
- **`UserBelongsToHospital`** — Maps users to the hospitals they can access.
- **`UserBelongsToRegion`** — Maps users to geographic regions.

### Group 5: Scheduling, Invoice, and Other Tables (Lines 834-1526)

These tables mirror the full production database schema. While not directly used by the AI engine, they exist so the ORM model is complete and can be used for future features:

- **Scheduling:** `HospitalSchedule`, `HospitalScheduleConfiguration`, `Scheduler`, `ScheduleDateList`, `ExemptedDates`, `HospitalDeliverySchedule`, `ScheduleReminder`, `ScheduleReminderRecipient`, `HospitalScheduleUnitSummary`
- **Invoicing:** `Invoice`, `InvoiceDetail`, `HospPricing`, `HospPricingNew`
- **Bags:** `Bag`, `CurtainBag`, `VisitBag`, `VisitBagScan`, `VisitBagLocation`, `BagReassignmentHistory`
- **Storage:** `TempStorageLocation`, `AIAutomationHospitalTempStorage`, `TblInStorage`
- **Issues:** `IssueTracker`, `IssueAttachment`
- **Maintenance:** `MaintainanceReport`
- **Remesh:** `RemeshOrder`, `RemeshOrderDetail`
- **Trucks:** `Truck`
- **Audit/History:** `WrongAttempt`, `DuplicateInstalledRecord`, `ScannedHistory`, `ScanComments`, `PerformAction`, `VisitMergeHistory`, `VisitDetailDeleted`, `VisitDetailRemoved`
- **Commissions:** `InstallerCommission`, `InstallerCommissions`, `InstCommTransaction`, `PaybyTrackCommission`
- **Other:** `Notification`, `LastLogin`, `LastSyncInfo`, `LocationDetailRecord`, `PendingEmail`, `VisitDropByUser`, `VisitVisitedBy`, `VisitInstallationImage`, `VisitPicture`, `VisitStorageInstallation`, `VisitTempStorage`

---

## 9. File: app/schemas.py — API Request/Response Shapes

**Purpose:** Defines the exact JSON structure of every API request and response using Pydantic models. Pydantic automatically validates incoming data and serializes outgoing data.

### ScanRequest (Line 6)

```python
class ScanRequest(BaseModel):
    curtain_barcode: str = Field(..., description="Barcode of the scanned curtain")
    visit_id: int | None = Field(None, description="Current visit ID if applicable")
    installer_id: int | None = Field(None, description="ID of the installer scanning")
```

**Logic:** Input for curtain scan. `curtain_barcode` is required (the `...` means no default). `visit_id` and `installer_id` are optional context that may be used for future features.

### LocationDetail (Line 12)

```python
class LocationDetail(BaseModel):
    hospital_name: str
    hospital_id: int
    building_name: str
    building_id: int
    floor: int
    unit_name: str
    unit_id: int
    room_name: str
    room_id: int
    track_barcode: str
    track_id: int
```

**Logic:** A complete location hierarchy. This is nested inside each recommendation, giving the installer the full path: Hospital > Building > Floor > Unit > Room > Track.

### TrackRecommendation (Line 26)

```python
class TrackRecommendation(BaseModel):
    rank: int
    location: LocationDetail
    score: float = Field(..., description="Confidence score 0-100")
    reason: str = Field(..., description="Why this track is recommended")
    type_match: bool
    style_match: bool
    size_match: bool
    has_capacity: bool
    warnings: list[str] = Field(default_factory=list)
```

**Logic:** One recommendation result. Fields:
- `rank` — Position in the list (1 = best match).
- `location` — The full LocationDetail (where to install).
- `score` — 0 to 100 confidence score from the scoring engine.
- `reason` — Human-readable explanation (e.g., "Score 78.5/100 — installed here 3 time(s) before; exact size match").
- `type_match`, `style_match`, `size_match`, `has_capacity` — Boolean flags used by the UI to show colored badges.
- `warnings` — List of warning messages (e.g., style mismatch, type mismatch, at capacity).

### SuggestLocationResponse (Line 38)

The full response for a curtain scan. Includes:
- Curtain metadata: barcode, status, category, hospital, disposable/spare flags
- `recommendations` — List of `TrackRecommendation` objects (up to 10)
- `total_candidates` — How many tracks were evaluated
- `message` — Summary text

### TrackScanRequest / CurtainMatch / MatchCurtainsResponse (Lines 50-80)

The reverse flow. `CurtainMatch` includes curtain barcode, type, dimensions, compatibility score, and whether it's the best match.

### RouteStopResponse / RouteSegmentResponse / InstallerRouteResponse (Lines 83-110)

Route optimization response. Organized hierarchically:
- `InstallerRouteResponse` contains segments (one per hospital)
- Each `RouteSegmentResponse` contains ordered stops
- Each `RouteStopResponse` has the full location details and pending curtain count

### CacheStatsResponse / HealthResponse (Lines 113-123)

Operational endpoints for monitoring.

---

## 10. File: app/cache.py — Caching Layer

### TTLCache Class (Line 15)

```python
class TTLCache:
    def __init__(self, default_ttl: int = 300):
        self._store: dict[str, tuple[Any, float]] = {}
        self._lock = threading.Lock()
        self._default_ttl = default_ttl
```

**Logic:** A thread-safe, in-memory cache with per-key TTL (Time-To-Live) expiration.

**Internal storage:** A dictionary where each key maps to a tuple of `(value, expiration_timestamp)`. For example: `{"rec:1001": ({"score": 85.0}, 1713052800.0)}`.

**Thread safety:** Uses a `threading.Lock()` to prevent race conditions when multiple API requests read/write the cache simultaneously.

**Methods:**

- **`get(key)`** — Acquires the lock, looks up the key. If found and not expired, returns the value. If expired, deletes the key and returns None.
- **`set(key, value, ttl)`** — Acquires the lock, stores the value with `expires_at = current_time + ttl`.
- **`delete(key)`** — Removes a single key.
- **`invalidate_prefix(prefix)`** — Removes all keys starting with a prefix. E.g., `invalidate_prefix("rec:")` removes all recommendation caches. Returns the count of removed keys.
- **`clear()`** — Removes everything.
- **`stats()`** — Returns total keys, expired-but-not-yet-cleaned keys, and active keys.

### RedisCache Class (Line 66)

**Logic:** Same interface as TTLCache but backed by Redis. Uses JSON serialization for values. The `try/except ImportError` pattern (line 63) means this class only exists if the `redis` Python package is installed.

- **`get(key)`** — Calls `redis.get()`, then JSON-deserializes the result.
- **`set(key, value, ttl)`** — JSON-serializes the value, calls `redis.setex()` with the TTL.
- **`invalidate_prefix(prefix)`** — Uses `redis.scan_iter()` to find matching keys, then deletes them in bulk.

### create_cache() Factory (Line 107)

```python
def create_cache(redis_url=None, default_ttl=300):
    if redis_url and RedisCache is not None:
        try:
            cache = RedisCache(url=redis_url, default_ttl=default_ttl)
            cache.get("__ping__")  # Test the connection
            return cache
        except Exception:
            pass
    return TTLCache(default_ttl=default_ttl)
```

**Logic:** Decision flow:
1. If Redis URL is provided AND the redis package is installed → try to create a RedisCache and test the connection.
2. If the connection works → use Redis.
3. If anything fails (bad URL, Redis not running, package not installed) → fall back to in-memory TTLCache.

### Cache Key Builders (Lines 128-141)

```python
def recommendation_key(curtain_barcode): return f"rec:{curtain_barcode}"
def track_counts_key(hospital_id):       return f"track_counts:{hospital_id}"
def match_curtains_key(track_barcode):   return f"match:{track_barcode}"
def route_key(installer_id, date_str):   return f"route:{installer_id}:{date_str}"
```

**Logic:** Standardized key naming ensures:
- Cache keys are unique and descriptive.
- Prefix-based invalidation works (e.g., `invalidate_prefix("rec:")` removes all recommendation caches).
- Keys include all parameters that affect the result (so different barcodes get different cache entries).

---

## 11. File: app/seed.py — Sample Data Generator

**Purpose:** Creates realistic test data in the SQLite database so the application can be tested locally without connecting to the real SQL Server or Snowflake database.

### Main Flow

1. **`seed()` function (line 35):** Entry point. Calls `init_db()` to create tables, checks if data already exists (idempotent — running seed twice doesn't duplicate data), then calls `_seed_data()`.

2. **Lookup tables (lines 57-116):** Creates:
   - 3 curtain types: Standard, Snap, Psyc
   - 3 track types: Straight, L-Shape, U-Shape
   - 6 width options: 36", 48", 60", 72", 84", 96"
   - 4 height options: 72", 84", 96", 108"
   - 5 curtain statuses: Curtain Setup, Clean, Soiled, Installed, Delivered
   - 2 grommet types: Standard, Snap
   - 9 unit types: ICU, General Ward, Surgical Ward, Recovery Wing, Emergency, Pediatrics, Cardiology, Maternity, Orthopedics

3. **Special hospitals (lines 118-127):**
   - Hospital 99: "AI Automation Hospital Disposable" — virtual hospital holding disposable curtains
   - Hospital 1001: "AI Automation Hospital Spare Curtains" — virtual hospital holding spare curtains

4. **Regular hospitals (lines 130-145):**
   - Hospital 1002: "Florida General Hospital" (account 1576)
   - Hospital 1003: "Orlando Regional Medical" (account 2301, has temp storage)
   - Hospital 1004: "Tampa Bay Community Hospital" (account 3042)

5. **Buildings/Units/Rooms/Tracks (lines 148-229):** Uses a nested specification dictionary:
   - Hospital 1002 gets 2 buildings ("Cancer Care Block" with 4 units, "Bone Block" with 2 units)
   - Hospital 1003 gets 1 building ("Main Building" with 3 units)
   - Hospital 1004 gets 1 building ("West Wing" with 3 units)
   - Each unit gets rooms, each room gets a track with randomized dimensions
   - Track barcodes follow the format `{account_number}-T{counter:04d}`

6. **Curtains (lines 231-299):**
   - Each hospital gets 3x as many curtains as tracks (realistic surplus)
   - 20 spare curtains assigned to Hospital 1001
   - 15 disposable curtains assigned to Hospital 99
   - Each curtain gets random type, width, height, and style

7. **Installation history (lines 301-337):** For each regular hospital curtain:
   - 2-8 historical installation records are created
   - 70% of installs go to a "primary" track (simulates the real pattern where curtains tend to go back to the same location)
   - 30% go to a "secondary" track (simulates occasional reassignment)
   - Install dates are spread across the past 180 days
   - This history is what makes the scoring engine produce meaningful ranked results

---

## 12. File: app/engine/rules.py — Business Rules (R1-R12)

**Purpose:** Implements AI Automation Hospital's hard business constraints. Every recommendation passes through these rules before being returned to the installer.

### Helper Functions

```python
def is_special_hospital(hospital): return hospital.HID in (99, 1001)
def is_disposable_curtain(curtain): return curtain.HID == 99
def is_spare_curtain(curtain): return curtain.HID == 1001
```

### Rule R1: Hospital-Bound Curtains (Line 30)

```python
def can_install_in_hospital(curtain, target_hospital_id):
    if curtain.HID in (99, 1001):
        return True
    return curtain.HID == target_hospital_id
```

**Logic:** A regular hospital's curtains can ONLY be installed within that same hospital. This prevents accidentally mixing Hospital A's curtains with Hospital B's. However, disposable curtains (Hospital 99) and spare curtains (Hospital 1001) are exceptions — they can go to any hospital because they're not hospital-specific.

### Rule R2: Packable Status (Line 41)

```python
def is_packable_status(cur_status_id, packable_ids):
    if not packable_ids: return True
    if cur_status_id is None: return True
    return cur_status_id in packable_ids
```

**Logic:** Only curtains in a "ready" state should be recommended for installation. If the packable set is empty (no configuration), allow all. If the curtain has no status, allow it (permissive default to avoid blocking due to missing data).

### Rule R4: Bag Capacity (Line 51)

```python
def bag_has_capacity(current_count):
    return current_count < 15
```

**Logic:** Each transport bag can hold at most 15 curtains. Simple count check.

### Rule R6: Track Barcode Belongs to Hospital (Line 56)

```python
def track_belongs_to_hospital(track_barcode, account_number):
    if account_number is None: return False
    return track_barcode.startswith(str(account_number))
```

**Logic:** Track barcodes are prefixed with the hospital's account number. E.g., "1576-T0001" belongs to the hospital with account 1576. If the barcode doesn't start with the account number, the track doesn't belong to that hospital.

### Rule R7: Style Mismatch Warning (Line 63)

```python
def check_style_match(curtain, unit):
    if curtain.UnitStyle is not None and unit.Style is not None:
        if curtain.UnitStyle != unit.Style:
            return "Style mismatch: curtain style ID ... but unit style ID ..."
    return None
```

**Logic:** Compares the curtain's intended style with the unit's preferred style. If they don't match, returns a warning string. Important: this is a **warning, not a block**. The installation is still allowed because sometimes style mismatches are acceptable (e.g., when exact matches aren't available).

### Rule R8: Type Mismatch Warning (Line 76)

```python
def check_type_match(curtain, track):
    if curtain.Curt_TypeID is not None and track.Curt_TypeId is not None:
        if curtain.Curt_TypeID != track.Curt_TypeId:
            return "Type mismatch: curtain is 'Snap' but track expects 'Standard'..."
    return None
```

**Logic:** Similar to R7 but for curtain type. A "Snap" curtain on a "Standard" track gets a warning. Not blocked because in practice, type mismatches sometimes work.

### Rule R9: Disposable Curtains Don't Need Bags (Line 95)

```python
def needs_bag(curtain):
    return not is_disposable_curtain(curtain)
```

**Logic:** Disposable curtains are single-use and don't go through the bag transport process.

### Rule R10: Temp Storage Hospital (Line 100)

```python
def is_temp_storage_hospital(hospital):
    return hospital.isTempStorage
```

**Logic:** Some hospitals have temporary storage areas where curtains can be staged before installation.

### Track Capacity Check (Line 105)

```python
def track_has_capacity(track, current_installed, curtain):
    max_regular = track.NumberOfCurtain or 0
    max_spare = track.NumberOfSpares or 0
    max_disposable = track.NumberOfDisposables or 0

    if is_disposable_curtain(curtain):
        return current_installed < max_disposable + max_regular
    if is_spare_curtain(curtain):
        return current_installed < max_spare + max_regular
    return current_installed < max_regular
```

**Logic:** Each track has a maximum capacity, but it varies by curtain type:
- **Regular curtains** are limited to `NumberOfCurtain` (e.g., 2 curtains max).
- **Disposable curtains** get additional capacity: `NumberOfCurtain + NumberOfDisposables` (e.g., 2 + 1 = 3 total).
- **Spare curtains** get additional capacity: `NumberOfCurtain + NumberOfSpares` (e.g., 2 + 1 = 3 total).

This allows tracks to hold their regular curtains plus extras when needed.

### Size Compatibility Check (Line 121)

```python
def size_compatible(curtain_width, track_length, tolerance=2.0):
    if curtain_width is None or track_length is None:
        return True
    return abs(curtain_width - track_length) <= tolerance
```

**Logic:** The curtain width must be within 2 inches of the track length. If either dimension is unknown (None), compatibility is assumed (no data should not penalize). The 2-inch tolerance accounts for manufacturing variations and measurement differences.

---

## 13. File: app/engine/scoring.py — Weighted Scoring Algorithm

**Purpose:** This is the brain of the recommendation system. It combines 6 different signals into a single 0-100 confidence score.

### Weights

```python
WEIGHTS = {
    "history":  0.35,  # 35% — how often this curtain went to this track before
    "size":     0.25,  # 25% — how close the curtain width matches the track length
    "type":     0.15,  # 15% — whether curtain type matches track type
    "style":    0.10,  # 10% — whether curtain style matches unit style
    "recency":  0.10,  # 10% — how recently this curtain was installed on this track
    "capacity": 0.05,  #  5% — whether the track still has room
}
```

**Logic:** History gets the highest weight (35%) because the most reliable predictor of where a curtain should go is where it has gone before. Size match gets 25% because a physically incompatible curtain is impractical. Type and style are important but less critical. Recency matters because if a curtain was recently installed somewhere, the installers likely intended to keep it there. Capacity gets the lowest weight because it's a binary constraint.

### ScoringInput Dataclass (Line 27)

```python
@dataclass
class ScoringInput:
    history_count: int        # times this curtain was installed on this track
    max_history: int          # highest install count across all tracks
    size_delta: float         # |curtain_width - track_length| in inches
    size_tolerance: float     # maximum acceptable delta (2.0 inches)
    type_match: bool          # curtain type == track type?
    style_match: bool         # curtain style == unit style?
    days_since_last_install: int | None  # days since most recent install on this track
    has_capacity: bool        # track has room for another curtain?
```

### compute_score() Function (Line 38)

**Logic — how each signal is converted to a 0-100 subscore:**

1. **History Score:** `(count / max_count) * 100`. If this curtain went to this track 5 times and the most-used track got 10 times, the history score is 50. This is relative scoring — the most-frequent track always gets 100.

2. **Size Score:**
   - Delta = 0 (exact match) → 100
   - Delta between 0 and tolerance (2") → linear decay from 100 to 0
   - Delta > tolerance → 0

3. **Type Score:** Match → 100, mismatch → 20. The mismatch is 20 (not 0) because type mismatches are allowed per Rule R8.

4. **Style Score:** Match → 100, mismatch → 30. The mismatch is 30 (not 0) because style mismatches are warned but not blocked per Rule R7.

5. **Recency Score:**
   - Last installed 0-7 days ago → 100 (very recent)
   - 8-30 days ago → 70
   - 31-90 days ago → 40
   - 91+ days ago → 10 (very stale)
   - No history → 50 (neutral)

6. **Capacity Score:** Has room → 100, full → 0.

**Final Score:** Weighted sum of all subscores, clamped to [0, 100], rounded to 1 decimal.

### build_reason() Function (Line 76)

**Logic:** Generates a human-readable explanation of the score. Collects applicable descriptions ("installed here 3 time(s) before", "exact size match", "type matches", etc.) and joins them into a sentence. Includes a WARNING if the track is at capacity.

---

## 14. File: app/engine/recommender.py — Curtain to Track Recommendation Engine

**Purpose:** Given a scanned curtain barcode, determines which track the curtain should be installed on, ranked by confidence score.

### Main Function: suggest_location() (Line 54)

**Step-by-step logic:**

**Step 1 — Parse barcode (lines 55-59):**
Try to convert the barcode string to an integer. Curtain barcodes in the database are stored as integers.

**Step 2 — Load curtain from database (lines 62-71):**
Query the `Hosp_Curtains` table with eager-loaded `hospital` relationship (so we get hospital data in one query, not two). If the barcode doesn't match any curtain, raise a `RecommenderError`.

**Step 3 — Get candidate tracks (line 77):**
The `_get_candidate_tracks()` function (line 214) runs a 5-table JOIN:
```
Hosp_Track → Hosp_Building_Rooms → Hosp_Unit → Hosp_Building → Hospital
```
This gives us each track with its full location hierarchy. Filters:
- Only enabled tracks (`Enabled = True`)
- Only enabled units (`Enabled = True`)
- **If regular curtain:** Only tracks in the same hospital (enforcing Rule R1)
- **If disposable or spare:** Tracks in ALL hospitals

**Step 4 — Get installation history (line 91):**
`_get_history_map()` queries `Track_Curtain_Services` for this curtain barcode, groups by `TrackBarCode`, counts occurrences, returns a dictionary like `{"1576-T0001": 5, "1576-T0002": 2}`. Limited to the top 50 tracks (`HISTORY_WINDOW_SIZE`).

**Step 5 — Get last install dates (line 93):**
`_get_last_install_dates()` finds the most recent `Installed_Date` per track for this curtain. Returns `{"1576-T0001": datetime(2026, 4, 10), "1576-T0002": datetime(2026, 3, 15)}`.

**Step 6 — Get installed counts (line 96):**
`_get_installed_counts()` counts how many curtains are currently installed on each candidate track. This is used for capacity checking.

**Step 7 — Score each candidate (lines 100-178):**
For every candidate track:
1. Calculate size delta: `|curtain_width - track_length|`
2. Check size compatibility using the 2-inch tolerance
3. Check type match: `curtain.Curt_TypeID == track.Curt_TypeId`
4. Check style match: `curtain.UnitStyle == unit.Style`
5. Calculate days since last install on this track
6. Build a `ScoringInput` with all signal values
7. Call `compute_score()` to get the 0-100 score
8. Call `build_reason()` to get the human-readable explanation
9. Check business rules and build warnings list:
   - Style mismatch warning (Rule R7)
   - Type mismatch warning (Rule R8)
   - At capacity warning
   - Size mismatch warning
10. Create a `TrackRecommendation` with full location details

**Step 8 — Sort and return (lines 180-203):**
Sort all recommendations by score (highest first), assign rank numbers (1, 2, 3...), return the top 10.

---

## 15. File: app/engine/match.py — Track to Curtain Matching Engine

**Purpose:** The reverse flow — given a scanned track barcode, finds all curtains that could be installed on it.

### Main Function: match_curtains_for_track() (Line 35)

**Logic:**

1. **Load track** from database by barcode. If not found, raise `MatchError`.
2. **Resolve location hierarchy:** Track → Room → Unit → Building → Hospital.
3. **Get candidate curtains:** All enabled curtains from:
   - The track's own hospital
   - Hospital 99 (disposable)
   - Hospital 1001 (spare)
4. **Score each curtain** against the track. Simpler than the recommender because there's no installation history (we don't know which curtain went to this track before). Scoring uses: size match, type match, style match. All candidates start with `has_capacity=True`.
5. **Sort by score, mark the best match, return top 15.**

---

## 16. File: app/engine/route.py — Installer Route Optimizer

**Purpose:** Given an installer's assigned visits for a day, produces an optimized visit order that minimizes back-and-forth between buildings and floors.

### Strategy (Nearest-Neighbor Heuristic)

1. Group all tracks to visit by hospital → building → floor
2. Order hospitals by total work (most tracks first — visit the busiest hospital first when the installer is freshest)
3. Within each hospital, visit buildings alphabetically, then top-to-bottom by floor
4. Within each floor, visit rooms in sequence

### Main Function: build_installer_route() (Line 64)

**Logic:**

1. **Find installer's tracks:** Query `Track_Curtain_Services` where `Installed_By` matches the installer ID. This finds all tracks the installer has historically serviced. Join to get full location data.
2. **Group by hospital:** Organize results into `{hospital_id: [list of track rows]}`.
3. **Sort hospitals:** Hospital with most tracks comes first.
4. **Sort within hospital:** By building name, then floor number, then room number. This creates a natural walk-through path.
5. **Build stops:** Each track becomes a numbered stop. `_count_pending_for_track()` counts pending service records.
6. **Build summary message:** E.g., "Route: Hospital A (4 tracks) -> Hospital B (2 tracks). 6 total stops."

---

## 17. File: app/agents/installation_agent.py — Cortex AI Agent

**Purpose:** The Snowflake Cortex AI integration layer. When an installer scans a curtain, this agent gathers data, builds a prompt, and calls an LLM to generate a plain-English explanation.

### Prompt Template (Line 40)

The prompt is carefully crafted to:
- Set the AI's role: "You are an AI installation assistant for AI Automation Hospital"
- Provide the scanned barcode
- Inject curtain details as JSON (type, style, hospital, dimensions)
- Inject installation history as JSON (where has this curtain gone before, how many times)
- Inject scored recommendations as JSON (the top 5 ranked results)
- List the business rules the AI must follow (R1, R7, R8, R9)
- Specify the exact output format:
  ```
  INSTALL HERE:
    Building : <name>
    Floor    : <number>
    Unit     : <ward/unit name>
    Room     : <room name>
    Track    : <track barcode>
    Confidence: <score>/100

  WHY: <1-2 sentences explaining the recommendation>

  WARNINGS: <list any style/type mismatches, or "None">
  ```

### run_agent() — Entry Point (Line 87)

**Step 1:** `_tool_lookup_curtain()` — Queries the curtain from the database and returns a dictionary with all relevant fields: ID, barcode, type, style, dimensions, weight, hospital, and flags (disposable, spare, mesh, manufacturing).

**Step 2:** `_tool_get_install_history()` — Joins `Track_Curtain_Services` with the full location hierarchy. Returns the 20 most recent installations with full context (hospital, building, unit, floor, room, track barcode, date). Also computes the top 3 most-frequently-used tracks using a `Counter`.

**Step 3:** `_tool_get_recommendations()` — Calls the full `suggest_location()` engine from `recommender.py` and formats the top 5 results as plain dictionaries for JSON serialization into the prompt.

**Step 4:** `_call_cortex()` — Assembles the prompt and calls the LLM.

### _call_cortex() — LLM Call (Line 111)

**Decision flow:**

1. Build the prompt by injecting all data into the template.
2. **If NOT on Snowflake** (`IS_SNOWFLAKE == False`): Return `_fallback_explanation()` — a template-based text response using the top recommendation data. No LLM call needed.
3. **If on Snowflake:**
   a. Import `snowflake.cortex.complete` (lazy import).
   b. Create a Snowpark session via `get_snowflake_session()`.
   c. If session creation fails → use fallback.
   d. Call `complete(CORTEX_MODEL, prompt, session=session)`.
   e. Return the LLM's response string.
   f. Always close the Snowpark session.
4. **Error handling:** ImportError (package not installed), any other exception → log warning and use fallback.

### _fallback_explanation() — No-LLM Response (Line 151)

**Logic:** Generates a structured response from the recommendation data without calling any LLM. Uses the exact same format as the LLM prompt requests, but fills it in mechanically from the top recommendation. Used in two scenarios:
1. Local development (no Snowflake connection)
2. Cortex AI failure (graceful degradation)

---

## 18. File: app/api/routes.py — All HTTP Endpoints

### POST /api/v1/agent/scan-curtain (Line 35)

**Purpose:** The full AI agent endpoint.
**Logic:** Calls `run_agent()` which does everything: curtain lookup + history + scoring + LLM explanation. Returns the raw dictionary with `curtain_barcode`, `recommendation`, and `agent_explanation`.
**Error handling:** Any exception returns HTTP 500 with the error message.

### POST /api/v1/suggest-location (Line 50)

**Purpose:** Deterministic recommendation (no LLM).
**Logic:**
1. Check the cache for this curtain barcode.
2. If cached → return immediately (fast path).
3. If not cached → run `suggest_location()` from the recommender engine.
4. Cache the result with a 120-second TTL.
5. Return the result.
**Error handling:** `RecommenderError` → HTTP 400. Pydantic validation error → HTTP 422.

### POST /api/v1/match-curtains (Line 84)

**Purpose:** Track-to-curtain matching.
**Logic:** Same cache-first pattern as suggest-location. Calls `match_curtains_for_track()`.

### GET /api/v1/installer/{installer_id}/route (Line 117)

**Purpose:** Route optimization.
**Logic:** Same cache-first pattern. Calls `build_installer_route()`. Converts the internal dataclass to the Pydantic response model.

### GET /api/v1/cache/stats (Line 181)

**Purpose:** Cache monitoring.
**Logic:** Returns the number of cached keys and which backend is active (in-memory or Redis).

### GET /api/v1/health (Line 197)

**Purpose:** Service health check.
**Logic:** Pings the database with `SELECT 1`, checks if the cache is initialized. Returns "ok" if both are up, "degraded" if either is down.

---

## 19. File: app/main.py — Application Entry Point

### Startup Sequence

```python
load_dotenv()  # Load .env file FIRST
```

**Logic:** This runs before any imports that depend on environment variables. It reads the `.env` file and sets all variables.

### Lifespan Context Manager (Lines 21-28)

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    cache = create_cache(redis_url=REDIS_URL, default_ttl=CACHE_DEFAULT_TTL)
    app.state.cache = cache
    yield
    cache.clear()
```

**Logic:**
- **On startup:** Create database tables (if SQLite), create the cache instance, store it in `app.state.cache` so all routes can access it.
- **`yield`** — The application runs and serves requests.
- **On shutdown:** Clear the cache.

### App Configuration (Lines 31-48)

```python
app = FastAPI(title="AI Automation Hospital AI Agent", version="0.4.0", lifespan=lifespan)
app.include_router(router, prefix="/api/v1", tags=["recommendations"])
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")
def root():
    return FileResponse(str(STATIC_DIR / "index.html"))
```

**Logic:**
- Creates the FastAPI app with metadata (shown in the auto-generated API docs at `/docs`).
- Mounts all API routes under the `/api/v1` prefix.
- Serves static files (CSS, JS, images) from `app/static/`.
- Serves the HTML UI at the root URL `/`.

---

## 20. File: app/static/index.html — Mobile-First Web UI

**Purpose:** A single-file web application designed for mobile use by installers in the field. No framework dependencies — pure HTML, CSS, and JavaScript.

### CSS (Lines 9-328)

- **Dark theme** with CSS custom properties (variables) for consistent theming.
- **Mobile-optimized:** `max-width: 480px`, sticky header and tabs, touch-friendly button sizes (48px minimum).
- **Score color coding:** Green (≥60), Yellow (≥35), Orange (<35).
- **Card-based layout** for results with badges, warnings, and location grids.

### HTML Structure (Lines 330-413)

Three tab panels:
1. **Scan Curtain** — Input field, camera button, "Where should I install this?" button, sample barcode quick-picks.
2. **Scan Track** — Same layout for track scanning.
3. **My Route** — Installer ID input, "Get My Route" button.

### JavaScript (Lines 416-676)

- **Tab switching:** Adds/removes `active` class.
- **Quick picks:** Sample barcode buttons auto-fill the input and trigger a scan.
- **`scanCurtain()`:** POSTs to `/api/v1/suggest-location`, renders result cards.
- **`scanTrack()`:** POSTs to `/api/v1/match-curtains`, renders matching curtains.
- **`loadRoute()`:** GETs `/api/v1/installer/{id}/route`, renders route segments.
- **Camera scanner:** Uses `html5-qrcode` library (loaded on-demand) to scan barcodes using the device camera.

---

## 21. File: demo.py — CLI Test Script

**Purpose:** A command-line script to test all API endpoints against a running server at `http://localhost:8000`.

**Logic:**
1. Opens the SQLite database directly to find sample barcodes.
2. Calls each endpoint and prints formatted results:
   - Health check
   - Curtain scan (regular, disposable, spare)
   - Track scan
   - Installer route
   - Cache stats

---

## 22. Test Files Overview

### test_rules.py — Business Rule Tests

Creates mock objects using helper functions and tests every rule:
- R1: Hospital-bound curtains (regular blocked, disposable/spare allowed)
- R2: Packable status filtering
- R4: Bag capacity limits (under 15, at 15, over 15)
- R6: Track barcode prefix matching
- R7: Style mismatch produces warning (not block)
- R8: Type mismatch produces warning (not block)
- R9: Disposable curtains don't need bags
- R10: Temp storage flag
- Track capacity with regular/disposable/spare curtains
- Size compatibility within/outside tolerance

### test_scoring.py — Scoring Algorithm Tests

- Perfect match scores ≥ 90
- No history reduces score
- Size mismatch reduces score
- No capacity penalized
- Type mismatch reduces score
- Scores always bounded [0, 100]
- Reason text includes history count and capacity warnings

### test_recommender.py — Recommender Integration Test

Seeds a complete hospital hierarchy in an in-memory SQLite database, then tests:
- Regular curtain gets recommendations
- Top recommendation is the most-frequently-used track
- Regular curtain only sees tracks in its own hospital
- Spare and disposable curtains can cross hospitals
- Unknown barcode raises error
- Results are sorted by score
- Style mismatches produce warnings

### test_match.py — Track Matching Integration Test

Seeds similar test data and tests:
- Returns matches for a known track
- Best match is flagged
- Spare curtains are included in candidates
- Type mismatches produce warnings
- Results sorted by score
- Unknown track raises error

### test_route.py — Route Optimization Test

Seeds 2 hospitals with multiple buildings, floors, rooms, and tracks. Tests:
- Route has stops for the known installer
- Route covers both hospitals
- Stops are globally ordered (1, 2, 3...)
- Unknown installer gets empty route
- Within-hospital stops are sorted by building then floor

### test_api_endpoints.py — HTTP Endpoint Tests

Uses FastAPI TestClient with SQLite in-memory database. Tests:
- `/suggest-location` — success, validation error (empty body → 422), domain error (bad barcode → 400)
- `/match-curtains` — success, validation error, domain error
- `/installer/{id}/route` — success, invalid date format
- `/cache/stats` — reflects API usage
- `/health` — ok when healthy, degraded when broken
- `/agent/scan-curtain` — success with mock, failure with mock

### test_cache.py — Cache Layer Tests

- Set/get, missing key returns None
- TTL expiration (waits 1.1 seconds, verifies expiry)
- Delete, prefix invalidation, clear
- Stats accuracy
- Key overwrite
- Factory falls back to in-memory when Redis unavailable

---

## 23. Snowflake Cortex AI — Plan and Pricing

### Which Plan to Buy

**Snowflake Standard Edition is sufficient.** Cortex AI (including COMPLETE/AI_COMPLETE, Cortex Search, Cortex Analyst, and Fine-tuning) is available on ALL editions:

| Edition | Cortex AI Access | Starting Price | Best For |
|---------|-----------------|---------------|----------|
| Standard | Full access | ~$3.90/credit | AI Automation Hospital's use case (cost-effective) |
| Enterprise | Full access | ~$5.85/credit | Multi-cluster compute, extended Time Travel |
| Business Critical | Full access | ~$7.00+/credit | HIPAA, PCI-DSS compliance |

**Recommendation:** Start with Standard Edition unless AI Automation Hospital handles PHI/PII data requiring HIPAA compliance — in that case, go with Business Critical.

### Pricing Model

- Token-based pricing (not compute credits)
- Small models (llama3.1-8b): ~0.0001-0.0005 credits/token — very cheap
- As of April 2026: new AI Credits at flat $2.00/credit
- Estimated cost for AI Automation Hospital: $10-50/month at moderate usage

### How to Get Started

1. Sign up at snowflake.com — 30-day free trial, no credit card
2. Choose AWS US East region for best Cortex AI availability
3. Grant the SNOWFLAKE.CORTEX_USER database role to your service account

---

## 24. Data Storage in Snowflake

### Core Tables Needed

| Table | Category | Data Volume | Change Frequency |
|-------|----------|-------------|-----------------|
| Hospital | Reference | Small (~100 rows) | Rare |
| Hosp_Building | Reference | Small (~500 rows) | Rare |
| Hosp_Unit | Reference | Small (~2000 rows) | Rare |
| Hosp_Building_Rooms | Reference | Small (~5000 rows) | Rare |
| Hosp_Track | Core | Medium (~20,000 rows) | Occasional |
| Hosp_Curtains | Core | Medium (~50,000 rows) | Regular |
| Track_Curtain_Services | Operational | Large (~500,000+ rows) | Very frequent |
| AI AUTOMATION HOSPITAL_USERS | Reference | Small (~200 rows) | Rare |

### Lookup Tables

All lookup tables (Curt_Type, Curt_Width, Curt_Height, Units, TrackType, etc.) should be mirrored in Snowflake. These are small and rarely change.

---

## 25. Data Required for AI Features

### For Curtain Scan (suggest-location)

**Input:** Curtain barcode (string)

**Data needed from database:**
1. Curtain record: type, style, width, height, hospital, flags
2. All tracks with full location hierarchy (filtered by hospital for regular curtains)
3. Installation history: which tracks this curtain has been installed on, how many times, most recent dates
4. Current installed counts per track (for capacity checking)

### For Track Scan (match-curtains)

**Input:** Track barcode (string)

**Data needed from database:**
1. Track record: type, length, height, location hierarchy
2. All available curtains from: same hospital + Hospital 99 + Hospital 1001

### For Route Optimization (installer route)

**Input:** Installer ID (integer) + optional date

**Data needed from database:**
1. All tracks the installer has historically serviced (from Track_Curtain_Services)
2. Full location hierarchy for each track

### For Cortex AI Explanation (agent scan)

**Input:** All of the above, assembled into a prompt

**Sent to Cortex:** Curtain details JSON + installation history JSON + top 5 recommendations JSON + business rules text

---

*End of Document*
