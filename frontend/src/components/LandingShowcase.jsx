import React from 'react';
import { Shield, Cpu, Layers, Zap, CheckCircle2, ArrowRight, Eye, FileText, BarChart3, Database } from 'lucide-react';

export default function LandingShowcase({ onStartScan }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '36px' }}>
      {/* Hero Banner */}
      <div className="glass-panel" style={{ padding: '40px', background: 'radial-gradient(ellipse at 50% 0%, rgba(56, 189, 248, 0.15) 0%, rgba(15, 23, 42, 0.6) 100%)', textAlign: 'center' }}>
        <div className="badge badge-cyan" style={{ marginBottom: '16px' }}>
          Document Fraud Detection Platform
        </div>
        <h1 style={{ fontSize: '2.2rem', fontWeight: '800', lineHeight: '1.2', maxWidth: '850px', margin: '0 auto 16px' }}>
          Automated First-Pass Forensic Triage & Adversarially Robust Verification
        </h1>
        <p style={{ fontSize: '1rem', color: 'var(--text-secondary)', maxWidth: '720px', margin: '0 auto 24px', lineHeight: '1.6' }}>
          DocShield AI ingests documents, extracts structured fields, detects pixel & metadata tampering, and outputs calibrated fraud risk scores with explainable heatmaps.
        </p>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '14px' }}>
          <button onClick={onStartScan} className="btn btn-primary" style={{ padding: '12px 28px', fontSize: '0.95rem' }}>
            <Shield size={18} />
            Try Document Scanner
            <ArrowRight size={16} />
          </button>
        </div>
      </div>

      {/* 4 Pillars Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '20px' }}>
        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ width: '42px', height: '42px', borderRadius: '10px', background: 'rgba(56,189,248,0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '16px' }}>
            <Eye size={22} color="#38bdf8" />
          </div>
          <h3 style={{ fontSize: '1.05rem', fontWeight: '700', marginBottom: '8px' }}>Visual Forgery Detection</h3>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: '1.5' }}>
            Vision Transformer (ViT) backbone + Error Level Analysis (ELA) spatial variance to catch copy-move, splicing, and compression artifacts.
          </p>
        </div>

        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ width: '42px', height: '42px', borderRadius: '10px', background: 'rgba(99,102,241,0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '16px' }}>
            <FileText size={22} color="#6366f1" />
          </div>
          <h3 style={{ fontSize: '1.05rem', fontWeight: '700', marginBottom: '8px' }}>Document Understanding</h3>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: '1.5' }}>
            LayoutLMv3 fine-tuned token tagging and type classification across IDs, Passports, Invoices, and Paystubs.
          </p>
        </div>

        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ width: '42px', height: '42px', borderRadius: '10px', background: 'rgba(16,185,129,0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '16px' }}>
            <Zap size={22} color="#10b981" />
          </div>
          <h3 style={{ fontSize: '1.05rem', fontWeight: '700', marginBottom: '8px' }}>Rule-Augmented Fusion</h3>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: '1.5' }}>
            Combines neural predictions with deterministic metadata checks (EXIF, font variance, arithmetic consistency) into an auditable risk score.
          </p>
        </div>

        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ width: '42px', height: '42px', borderRadius: '10px', background: 'rgba(245,158,11,0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '16px' }}>
            <BarChart3 size={22} color="#f59e0b" />
          </div>
          <h3 style={{ fontSize: '1.05rem', fontWeight: '700', marginBottom: '8px' }}>Adversarial Benchmarks</h3>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: '1.5' }}>
            Evaluates robustness across Easy, Medium, and Hard tiers with held-out generalization testing and measured F1 / AUROC metrics.
          </p>
        </div>
      </div>

      {/* Interactive System Flow Diagram */}
      <div className="glass-panel" style={{ padding: '30px' }}>
        <h3 style={{ fontSize: '1.15rem', fontWeight: '700', marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Layers size={20} color="#38bdf8" />
          End-to-End Pipeline Architecture
        </h3>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '24px' }}>
          Modular multi-stage pipeline with independent versioning and hot-swappable model checkpoints.
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '12px' }}>
            <div style={{ background: 'var(--bg-tertiary)', padding: '16px', borderRadius: '10px', border: '1px solid var(--border-subtle)', textAlign: 'center' }}>
              <div style={{ fontSize: '0.75rem', color: '#38bdf8', fontWeight: '700' }}>1. INGESTION</div>
              <div style={{ fontSize: '0.85rem', color: '#ffffff', fontWeight: '600', marginTop: '4px' }}>PDF / Image Rasterizer</div>
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px' }}>Deskew, MIME filter, normalization</div>
            </div>

            <div style={{ background: 'var(--bg-tertiary)', padding: '16px', borderRadius: '10px', border: '1px solid var(--border-subtle)', textAlign: 'center' }}>
              <div style={{ fontSize: '0.75rem', color: '#38bdf8', fontWeight: '700' }}>2. OCR & LAYOUT</div>
              <div style={{ fontSize: '0.85rem', color: '#ffffff', fontWeight: '600', marginTop: '4px' }}>TrOCR / LayoutLMv3</div>
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px' }}>Token extraction & 2D bboxes</div>
            </div>

            <div style={{ background: 'var(--bg-tertiary)', padding: '16px', borderRadius: '10px', border: '1px solid var(--border-subtle)', textAlign: 'center' }}>
              <div style={{ fontSize: '0.75rem', color: '#38bdf8', fontWeight: '700' }}>3. UNDERSTANDING</div>
              <div style={{ fontSize: '0.85rem', color: '#ffffff', fontWeight: '600', marginTop: '4px' }}>Schema Field Parser</div>
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px' }}>Type classifier & typed KVs</div>
            </div>

            <div style={{ background: 'var(--bg-tertiary)', padding: '16px', borderRadius: '10px', border: '1px solid var(--border-subtle)', textAlign: 'center' }}>
              <div style={{ fontSize: '0.75rem', color: '#38bdf8', fontWeight: '700' }}>4. FORGERY DETECTOR</div>
              <div style={{ fontSize: '0.85rem', color: '#ffffff', fontWeight: '600', marginTop: '4px' }}>ViT + ELA Head</div>
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px' }}>Attention rollout heatmaps</div>
            </div>

            <div style={{ background: 'var(--bg-tertiary)', padding: '16px', borderRadius: '10px', border: '1px solid var(--border-subtle)', textAlign: 'center' }}>
              <div style={{ fontSize: '0.75rem', color: '#38bdf8', fontWeight: '700' }}>5. RISK FUSION</div>
              <div style={{ fontSize: '0.85rem', color: '#ffffff', fontWeight: '600', marginTop: '4px' }}>Bayesian Fusion</div>
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px' }}>Calibrated 0-1 risk score</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
