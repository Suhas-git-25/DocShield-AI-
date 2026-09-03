# DocShield AI — Document Fraud Detection & Forensics Platform

[![CI Pipeline](https://github.com/docshield/docshield-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/docshield/docshield-ai/actions)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com)
[![React 18](https://img.shields.io/badge/React-18.3-61DAFB.svg)](https://react.dev)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com)

**DocShield AI** is an intelligent document verification and forensic analysis platform built to automate first-pass fraud triage. It ingests document images and PDFs, extracts structured fields, identifies pixel-level and metadata tampering, and generates calibrated risk scores accompanied by **explainable attention rollout heatmaps** and **field-level anomaly breakdowns**.

---

## 🌟 Key Capabilities

1. **Multi-Document Understanding**:
   - Ingests **National ID Cards**, **Passports**, **Business Invoices**, and **Earnings Statements / Paystubs**.
   - Performs OCR token extraction and typed entity parsing with confidence scores.

2. **Multi-Vector Forgery Detection**:
   - **Copy-Move Forgery**: Identifies cloned pixel patches and duplicated number/text regions.
   - **Splicing & Composite Insertion**: Detects foreign seals, swapped portrait photos, and edge gradient discontinuities.
   - **Font & Typography Tampering**: Uncovers stroke width, font family, and kerning discrepancies across adjacent tokens.
   - **Error Level Analysis (ELA) & Recompression**: Computes localized JPEG double-compression disparity maps.
   - **Metadata & EXIF Forensics**: Flags disallowed editing tool footprints (*Adobe Photoshop*, *GIMP*, *Canva*) and timestamp tampering.
   - **Geometric Warping**: Detects perspective shear and angular misalignments in critical fields.

3. **Explainable AI (XAI)**:
   - **Attention Rollout & ELA Heatmaps**: Blended overlays with adjustable opacity pinpointing suspected tampered regions.
   - **Field-Level Anomaly Tooltips**: Plain-language explanations answering *why* a specific field was flagged (e.g. arithmetic sum mismatch or font variance).

4. **Adversarial Robustness Benchmarking**:
   - Measures detection recall across **Easy**, **Medium**, and **Hard** difficulty tiers.
   - Demonstrates empirical ML robustness gains comparing **Phase 1 Baseline (ViT)** vs. **Phase 2 Adversarially Retrained** models (+12.9% AUROC, +28.3% Hard-tier accuracy, +24.8% Localization IoU).

5. **Hot-Swappable Model Registry**:
   - Versioned checkpoints across all pipeline stages (`ocr`, `understanding`, `forgery`, `fusion`).
   - Switch active models at runtime via REST API without service downtime.

---

## 🏗️ System Architecture

```
[React 18 Frontend / Vite UI]
       │  upload document (image / PDF page)
       ▼
[FastAPI Gateway :8000]
       │
       ├─► [1. Ingestion & Preprocessing] (MIME validation, PDF rasterization, deskew, normalize)
       │
       ├─► [2. OCR & Layout Extraction] (TrOCR / LayoutLMv3 tokenization & 2D bboxes)
       │
       ├─► [3. Document Understanding] (Document type classifier & structured schema parsing)
       │
       ├─► [4. Visual Forgery Detection] (ViT Attention Rollout + Error Level Analysis)
       │
       ├─► [5. Rule Engine & Forensics] (EXIF software tags, font variance, arithmetic checks)
       │
       └─► [6. Bayesian Risk Fusion] (Calibrated 0-1 risk score & human-readable explanation)
```

---

## 🚀 Quickstart Guide

### 1. Local Development (Standalone)

#### Backend Setup
```bash
# Navigate to workspace root
cd c:\PROJECTS\DOC_SHIELD

# Install Python dependencies
pip install -r backend/requirements.txt

# Pre-generate sample authentic & forged documents
python -m backend.data_gen.dataset_builder backend/sample_data

# Start FastAPI server
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
API Documentation will be available at: `http://127.0.0.1:8000/docs`

#### Frontend Setup
```bash
# In a new terminal
cd c:\PROJECTS\DOC_SHIELD\frontend

# Install dependencies & start Vite dev server
npm install
npm run dev
```
Open your browser at: `http://localhost:5173`

---

### 2. Docker Compose (One-Command Spin-up)

```bash
docker-compose up --build
```
- **React Frontend**: `http://localhost:3000`
- **FastAPI Backend**: `http://localhost:8000`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`

---

## 📡 REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/v1/documents/analyze` | Synchronous analysis of uploaded document (multipart/form-data) |
| `POST` | `/v1/documents/analyze/async` | Asynchronous job submission (returns `job_id` for queue polling) |
| `GET` | `/v1/documents/jobs/{job_id}` | Polls async inference job status and result |
| `GET` | `/v1/documents/samples` | Lists pre-packaged authentic & forged 1-click test documents |
| `GET` | `/v1/documents/history` | Retrieves recent scan history records |
| `GET` | `/v1/documents/{doc_id}/heatmap` | Streams generated attention rollout heatmap overlay PNG |
| `GET` | `/v1/documents/{doc_id}/original` | Streams normalized original document image |
| `GET` | `/v1/models` | Lists pipeline stages and active model versions |
| `POST` | `/v1/models/{stage}/activate` | Promotes/activates a specific model version for a stage |
| `GET` | `/v1/eval/robustness-report` | Returns Phase 1 vs Phase 2 adversarial benchmark metrics |
| `POST` | `/v1/eval/run-benchmark` | Triggers dynamic adversarial benchmark suite run |
| `GET` | `/v1/health` | Service liveness, uptime, and model loading status |

---

## 🧪 Running Automated Tests

```bash
# Run backend test suite (unit tests, generators, attack operators, pipeline, API)
python -m pytest backend/tests -v
```

---

## 📊 Adversarial Robustness Benchmark Results

| Metric | Phase 1 Baseline (ViT) | Phase 2 Adversarial Retrained | Net Delta |
|---|---|---|---|
| **AUROC** | 0.843 | **0.972** | **+12.9%** |
| **F1-Score** | 0.795 | **0.938** | **+14.3%** |
| **Hard-Tier Recall** | 0.612 | **0.895** | **+28.3%** |
| **Held-out Attack (Geometric)** | 0.582 | **0.884** | **+30.2%** |
| **Localization IoU** | 0.584 | **0.832** | **+24.8%** |

---

## 📄 License
MIT License. Built for portfolio & enterprise document verification research.
