# DocShield AI — Document Fraud Detection Platform
### Requirements & Technical Design Document

**Stack:** Python, PyTorch, Hugging Face, FastAPI, React, Docker
**Project type:** Portfolio / interview showcase
**Document types in scope:** ID/Passport, Invoice/Pay Stub

---

## 1. Product Overview & Scope

### Problem Statement
Manual document verification (IDs, invoices, contracts, certificates) is slow, inconsistent, and easy to fool with modern editing tools. DocShield AI automates first-pass fraud triage: it ingests a document image, extracts and understands its content, flags visual/structural signs of tampering, and returns a risk score with human-readable explanations — so a human reviewer only needs to look closely at the documents that actually warrant it.

### Target Users
- **Fintech / lending ops teams** — verifying pay stubs, bank statements, ID documents during onboarding
- **HR / background-check platforms** — verifying diplomas, certificates, employment letters
- **Insurance claims teams** — verifying receipts, invoices submitted with claims

### In Scope
- Single-document upload (image or PDF page) → structured extraction → forgery risk assessment
- Document types: **ID/Passport** and **Invoice/Pay Stub**
- Forgery types detected: copy-move/splicing, font/text inconsistency, recompression artifacts, metadata mismatches
- Explainability: region-level heatmap + field-level anomaly notes
- Adversarial robustness benchmarking as a first-class, demoable feature
- REST API + React frontend for upload and review
- Framer landing page for portfolio presentation

### Out of Scope
- Multi-page PDF workflows, batch processing at scale
- Real identity verification (liveness checks, biometric matching)
- Legal/compliance certification of fraud findings
- Multi-language OCR beyond English (future work)
- Full production auth/user-management system (minimal API key is sufficient)

### Success Criteria
- **Functional:** end-to-end pipeline runs on a real uploaded document and returns risk score + explanation in a demoable UI
- **ML:** measurable robustness improvement (before/after adversarial training) with clear metrics (F1, AUROC) and charts
- **Engineering:** dockerized, one-command spin-up, visible model versioning (MLflow), documented API (OpenAPI/Swagger)
- **Narrative:** every design decision is defensible in an interview — depth over breadth

---

## 2. System Architecture

### High-Level Flow

```
[React Frontend]
      │  upload document (image/PDF page)
      ▼
[FastAPI Gateway] ──────────────────────────────────────────┐
      │                                                       │
      ▼                                                       │
[1. Ingestion & Preprocessing]                                │
   - file validation, PDF→image, deskew, resize, normalize    │
      │                                                        │
      ▼                                                        │
[2. OCR / Layout Extraction]  (TrOCR / LayoutLMv3)             │
   - extract text + bounding boxes + field structure           │
      │                                                         │
      ▼                                                         │
[3. Document Understanding]  (LayoutLMv3 fine-tuned)            │
   - classify doc type, parse key fields (name, date, amount…)  │
      │                                                         │
      ▼                                                         │
[4. Forgery Detection]  (ViT/ConvNeXt head + rule checks)       │
   - visual tamper detection (splicing, font mismatch, ELA)     │
   - metadata/consistency checks (EXIF, font consistency)       │
      │                                                         │
      ▼                                                         │
[5. Risk Scoring & Fusion]                                      │
   - combine model scores + rule-based signals → single score   │
   - generate explanation payload (heatmap regions, flagged     │
     fields, contributing signals)                              │
      │                                                          │
      ▼                                                          │
[Response: JSON — extracted fields, risk score, explanations] ──┘
      │
      ▼
[React Frontend: results view, heatmap overlay, field table]

     (offline / side path, not per-request)
[Adversarial Eval Pipeline] → generates synthetic forged docs
      → feeds Data Strategy + benchmarks Forgery Detection model
      → results tracked in experiment tracker (MLflow)
```

### Component Boundaries

| Component | Responsibility | Owns |
|---|---|---|
| Ingestion Service | Validate + normalize input | File format, size limits, PDF rasterization |
| OCR/Layout Module | Turn pixels into structured text+boxes | TrOCR/Donut + LayoutLMv3 inference |
| Understanding Module | Map raw extraction → typed fields | Field schema per doc type, confidence scores |
| Forgery Detection Module | Visual + metadata tamper signals | ViT head inference, ELA, EXIF checks |
| Risk Fusion Module | Combine all signals into one verdict | Weighting logic, explanation generation |
| API Layer (FastAPI) | Orchestrate the above, expose endpoints | Request/response contracts, async job handling |
| Frontend (React) | Upload, display results, show explainability | UI state, heatmap rendering, review workflow |
| Adversarial Eval Pipeline | Offline: generate attacks, benchmark robustness | Synthetic data gen, eval scripts, reports |
| MLOps Layer | Track experiments, version models | Docker, MLflow, model registry |

### Key Architectural Decisions
- **Modular pipeline, not one giant model** — each stage independently testable/replaceable
- **Explicit, rule-augmented fusion layer** — not "trust the neural net"; realistic and auditable for fraud systems
- **Adversarial pipeline decoupled from the live request path** — training/benchmarking loop, not real-time
- **Async-capable inference** — supports "submit → poll" in addition to a synchronous demo path

---

## 3. Data Strategy

Real fraud-labeled documents are essentially impossible to source (privacy, legal, scarcity). The approach: use public/synthetic "clean" documents as ground truth, then programmatically generate the forgeries.

### 3.1 Source ("Clean/Authentic") Documents

| Doc Type | Source | Why |
|---|---|---|
| ID/Passport | `MIDV-500` / `MIDV-2019` (public synthetic ID dataset built for this research purpose) | Purpose-built, legally clean, no real PII |
| Invoice/Pay stub | Programmatically generated via HTML/CSS templates rendered to image (`weasyprint`/`wkhtmltopdf`), populated with **Faker** | No clean public dataset exists; full control over layout and labeling |

### 3.2 Synthetic Forgery Generation Pipeline

| Attack Type | Method | Simulates |
|---|---|---|
| Copy-move | Copy a region, paste elsewhere with slight offset/blend | Duplicating pixels to alter a number/date |
| Splicing | Composite a region from a different document | Swapping a photo, signature, or logo |
| Text/font tampering | Re-render a text field in a different font/size, paste over original | Editing a name, amount, or date |
| Recompression artifacts | Re-save at varying JPEG quality, especially on a sub-region | Screenshot-and-edit patterns |
| Metadata tampering | Strip/alter EXIF, inconsistent creation-tool metadata | Edited-but-disguised-as-original documents |
| Geometric tampering | Slight warp/rotate a sub-region independently | Poor manual splicing missing perspective alignment |

Each sample carries: `{original_id, attack_type, attack_region_bbox, severity_level}`.

### 3.3 Labeling Scheme
- **Document-level:** `authentic` / `forged`
- **Forgery-type** (multi-class, forged only): one of the 6 attack types
- **Region label:** bounding box(es) of tampered area
- **Field-level:** typed key-value pairs (name, dob, id_number, amount, date) with confidence

### 3.4 Splits
- Split by **source document identity first**, then apply attacks — no identity leakage across splits
- 70% train / 15% val / 15% test
- **One attack type held out entirely from training**, kept only in test — enables an honest generalization claim

### 3.5 Volume Target
- ~500–1,000 clean base documents across both doc types
- ~3–5 forged variants per clean doc → ~2,000–5,000 total labeled images

---

## 4. ML Models & Pipeline

### 4.1 Stage-by-Stage Model Selection

| Stage | Model | Fine-tuning Strategy |
|---|---|---|
| OCR | `microsoft/trocr-base-printed` | Off-the-shelf initially; fine-tune only if error analysis shows systematic failures |
| Layout/Document Understanding | `microsoft/layoutlmv3-base` | Fine-tune classification + token-tagging heads (doc-type classification, BIO field tagging) |
| Visual Forgery Detection | `google/vit-base-patch16-224-in21k` | Freeze bottom ~8 layers, fine-tune top layers + new head on authentic/forged + attack-type labels |
| Region Localization | Same ViT backbone + lightweight head, or attention-rollout | Trained against attack bounding-box labels |
| Metadata/Rule Checks | No model — deterministic Python | EXIF parsing, checksum validation, date sanity, font-consistency variance checks |

### 4.2 Training Approach
- **Two-phase fine-tuning:**
  1. Phase 1 — train on base synthetic forgery dataset
  2. Phase 2 — **adversarial fine-tuning**: after benchmarking exposes weak spots, generate targeted attacks, retrain, re-benchmark
- Use Hugging Face `Trainer` API for speed of implementation
- Every run tracked (hyperparameters, dataset version, attack config, metrics, checkpoints)

### 4.3 Explainability Method
- **Attention rollout** on the ViT forgery-detection model — aggregates attention weights into a heatmap, no extra training needed
- **Field-level anomaly flags** from the rule layer — plain-language reasons (e.g., "amount field font differs from surrounding text")
- Together: heatmap answers "where," rule explanation answers "why"

### 4.4 Model Versioning
Every fine-tuned checkpoint is tagged with: dataset version + attack-generation config + training run ID — enabling controlled rollout/rollback via the model registry.

---

## 5. Adversarial Evaluation Pipeline

### 5.1 Pipeline Structure

```
[Clean Doc Pool]
      │
      ▼
[Attack Generator]  ← config-driven (attack type, severity, region strategy)
      │
      ▼
[Attack Test Suite]  (held-out, versioned, never used in training)
      │
      ▼
[Model Under Test]  (a specific checkpoint version)
      │
      ▼
[Metrics Collector]  → per-attack-type breakdown
      │
      ▼
[Robustness Report]  → logged to MLflow, rendered as charts
```

### 5.2 Difficulty Tiers

| Tier | Description | Example |
|---|---|---|
| Easy | Obvious artifacts | High-severity splice, mismatched font size |
| Medium | Realistic tampering | Blended copy-move, moderate recompression |
| Hard / adversarial | Designed to fool the model | Low-severity edits, held-out attack type |

### 5.3 Metrics

| Metric | What it measures |
|---|---|
| Accuracy / F1 | Overall detection performance |
| AUROC / AUPRC | Threshold-independent discrimination |
| Per-attack-type recall | Detection rate broken down by attack type |
| Localization IoU | Overlap between predicted and ground-truth tamper region |
| Robustness delta | Metric drop from Easy → Hard tier |
| Generalization gap | Performance on held-out vs. seen attack types |

### 5.4 Benchmarking Loop
1. Run Phase 1 model against full attack suite → baseline robustness report
2. Identify weakest attack type(s)/tier(s)
3. Generate additional targeted synthetic attacks for weak spots
4. Fine-tune Phase 2 model
5. Re-run the same frozen benchmark suite → compare before/after
6. Repeat once more if time allows

### 5.5 Reporting Artifacts
- `robustness_report.json` per run (machine-readable, feeds MLflow)
- Rendered comparison chart (per-attack-type recall, before vs after)
- Auto-generated markdown summary per run

---

## 6. Backend (FastAPI) Design

### 6.1 API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/v1/documents/analyze` | POST | Submit a document (sync path) |
| `/v1/documents/analyze/async` | POST | Submit a document (async path) — returns `job_id` |
| `/v1/documents/jobs/{job_id}` | GET | Poll job status/result |
| `/v1/documents/{doc_id}/explain` | GET | Return heatmap + field-level explanations |
| `/v1/models` | GET | List available model versions per stage |
| `/v1/models/{stage}/activate` | POST | Switch active model version for a stage |
| `/v1/eval/robustness-report` | GET | Return latest/historical adversarial benchmark report |
| `/v1/health` | GET | Liveness/readiness check |

### 6.2 Request/Response Schemas (Pydantic)

```python
# Request
class AnalyzeRequest(BaseModel):
    document_type_hint: Optional[Literal["id_card", "invoice", "paystub"]] = None
    # file itself comes via multipart/form-data, not JSON body

# Response
class FieldResult(BaseModel):
    field_name: str
    value: str
    confidence: float
    anomaly_flag: bool
    anomaly_reason: Optional[str]

class ForgerySignal(BaseModel):
    attack_type_guess: Optional[str]
    confidence: float
    region_bbox: Optional[List[float]]  # [x1, y1, x2, y2] normalized

class AnalyzeResponse(BaseModel):
    doc_id: str
    document_type: str
    risk_score: float  # 0-1
    risk_level: Literal["low", "medium", "high"]
    fields: List[FieldResult]
    forgery_signals: List[ForgerySignal]
    heatmap_url: Optional[str]
    model_versions: dict[str, str]  # {"ocr": "v1", "forgery": "v2", ...}
    processing_time_ms: int

class JobStatus(BaseModel):
    job_id: str
    status: Literal["queued", "processing", "completed", "failed"]
    result: Optional[AnalyzeResponse]
```

### 6.3 Async Inference Pattern
- **Redis + RQ** for the job queue (lighter than Celery, still demonstrates a real async pattern)
- Flow: `POST /analyze/async` → save file → enqueue job → return `job_id` → worker runs pipeline → writes result → client polls `/jobs/{job_id}`

### 6.4 Model Serving & Versioning
- Each stage's model loaded once at startup, referenced by version tag from the MLflow registry
- Model files in `models/{stage}/{version}/` structure
- `/v1/models/{stage}/activate` allows runtime version swap without redeploying

### 6.5 Error Handling & Validation
- File type/size validation at ingestion → `422`
- Pipeline failures return structured `500`, never a raw stack trace
- Sync endpoint timeout → error response suggests the async endpoint

---

## 7. Frontend (React) Design

### 7.1 Key Screens

| Screen | Purpose |
|---|---|
| Upload / Analyze | Drag-and-drop, doc-type hint, submit, loading/job-tracking state |
| Document Result View | Fields table, risk score badge, heatmap overlay, explanations, model version footer |
| Document History | List of previously analyzed docs, filterable |
| Analytics Dashboard | Robustness reports, per-attack-type recall charts, model comparison, aggregate risk distribution |
| Model Registry View | Model versions per stage, active version indicator, activate control |

### 7.2 Document Result View
- **Heatmap overlay**: attention-rollout heatmap on original image, toggleable
- **Fields table**: value + confidence + inline anomaly flag with tooltip reason
- **Risk score badge**: color-coded (green/amber/red) with a one-line plain-language summary of top contributing signals

### 7.3 Analytics Dashboard
- **Robustness comparison chart**: grouped bar chart, per-attack-type recall, model version A vs B
- **Difficulty tier breakdown**: Easy/Medium/Hard performance view
- **Aggregate operational view**: risk-level distribution over time, kept visually separate from ML-eval charts (e.g., tabs: "Model Performance" vs "Document Activity")
- **Model version selector**: dropdown to compare checkpoint reports interactively
- **Seed with real benchmark data** so the dashboard is never empty in a demo

### 7.4 State & Data Fetching
- **React Query** for server state and async job polling (`refetchInterval`)
- Components: `UploadForm`, `ResultView` (`FieldsTable`, `HeatmapOverlay`, `RiskBadge`), `Dashboard` (`RobustnessChart`, `TierBreakdown`, `ActivityChart`, `ModelSelector`)
- **Recharts** for grouped bar/line/area charts

### 7.5 Visual/UX Note
Clean, clinical design language — muted palette, risk-level colors as the only strong accents, clear typographic hierarchy.

### 7.6 Landing Page (Framer) — Integration
- **Decoupled from the app**: Framer publishes as a static site; the functional app is a separate deployable
- **Subdomain split**: `docshield.ai` (Framer landing) → CTA links to `app.docshield.ai` (React app). No proxy complexity.
- **Landing page content**: problem/solution framing, pipeline visual walkthrough, embedded robustness chart image, "Try the demo" CTA, tech stack badges, links to GitHub repo + architecture diagram
- No API calls from Framer — purely static/marketing; optional "request access" form via Framer's built-in form + webhook

---

## 8. MLOps & Infra

### 8.1 Containerization (Docker)

```
docker-compose.yml
├── api            (FastAPI app)
├── worker         (RQ worker — async inference jobs)
├── redis          (job queue + result cache)
├── postgres       (metadata: doc history, job records, model registry entries)
├── mlflow         (experiment tracking + model registry UI)
└── frontend       (React app, served via nginx or static build)
```
- `api` and `worker` share a base image (same model-loading code, different entrypoint)
- Models mounted as a volume, not baked into the image
- `docker-compose up` brings up the entire stack

### 8.2 Experiment Tracking
**MLflow** (self-hosted, built-in model registry, no external API key needed)
- Log per run: hyperparameters, dataset version, attack config, metrics, robustness report artifact
- Promote best checkpoint to registry with stage tag (`Staging` → `Production`)
- Compare Phase 1 vs Phase 2 runs side-by-side in the UI

### 8.3 Model Registry Mechanics
- Each pipeline stage has its own registered model name (e.g., `docshield-forgery-vit`)
- Version numbers auto-increment on promotion
- `/v1/models` queries MLflow's registry API; `/activate` calls `transition_model_version_stage`

### 8.4 CI/CD

```
.github/workflows/ci.yml
├── on: push/PR
├── lint + type-check (ruff/mypy backend, eslint frontend)
├── unit tests (pytest — schema validation, rule checks, API contracts)
├── build Docker images
└── (optional) smoke-test: docker-compose up, hit /health, tear down
```
- Full model retraining explicitly excluded from CI — handled via a separate manual/scheduled workflow

### 8.5 Monitoring
- `/v1/health` checks: models loaded, Redis reachable, DB reachable
- Structured JSON logs of latency + model versions per request
- Prometheus/Grafana noted as future work, not built

---

## 9. Non-Functional Requirements

### 9.1 Performance

| Target | Value |
|---|---|
| Sync endpoint latency | < 5s p95 CPU, < 1.5s GPU |
| Async job turnaround | < 15s under normal load |
| Frontend load time | < 2s to interactive |
| Concurrent load | Designed for ~5–10 concurrent requests |

### 9.2 Security & Privacy
- No real PII ever enters the system (synthetic data only)
- Uploaded documents auto-deleted after 24–48h, never logged in plaintext
- API key/token auth on write endpoints
- Input validation hardened against path traversal, oversized files, decompression bombs
- HTTPS enforced at the deployment/hosting layer

### 9.3 Explainability & Auditability
- Every risk score traceable to specific contributing signals
- Model version persisted with every result

### 9.4 Reliability
- Graceful degradation if forgery model fails (`"forgery_analysis": "unavailable"` rather than full failure)
- Idempotency via hash-based dedup of resubmitted documents

### 9.5 Cost Constraints
- Training: single consumer GPU / free-tier Colab T4
- Inference: CPU-only in the deployed demo
- Hosting: free/cheap tiers (Vercel/Netlify, Render/Fly.io/Railway), MLflow self-hosted

---

## 10. Roadmap / Build Phases

| Phase | Focus | Checkpoint |
|---|---|---|
| 0 — Foundations | Repo scaffolding, docker-compose skeleton, CI skeleton, data sourcing | Can generate N clean synthetic documents on demand |
| 1 — Data & Attack Pipeline | Build all 6 attack types, generate labeled dataset with splits | Dataset artifact with clean/forged pairs + bbox labels |
| 2 — Core ML Pipeline (v1) | Off-the-shelf TrOCR + LayoutLMv3, rule-based checks | Script prints extracted fields + rule flags on an image |
| 3 — Forgery Detection Model | Fine-tune ViT (Phase 1), first adversarial benchmark | First `robustness_report.json` + chart |
| 4 — Backend API | FastAPI sync endpoint end-to-end, then async path | `curl`-able API returning full `AnalyzeResponse` |
| 5 — Adversarial Retrain Loop | Targeted data on weak spots, retrain, re-benchmark | Before/after chart proving robustness improvement (flagship artifact) |
| 6 — MLOps Wiring | MLflow stood up, model registry wired to API, full docker-compose | One-command spin-up, models served from registry |
| 7 — Frontend | Upload/Result View → Dashboard → Model Registry View | Full click-through demo with real charts |
| 8 — Landing Page & Polish | Framer landing page, CI finalized, README, demo video | Shareable link + repo ready for a resume |

**Pacing guidance:** Phases 0–4 = "make it work," Phase 5 = "make it good" (the core ML differentiation), Phases 6–8 = "make it presentable." If time is short, trim Phase 8 polish before ever trimming Phase 5.

---

*Document compiled iteratively, section by section, as the working spec for the DocShield AI portfolio build.*
