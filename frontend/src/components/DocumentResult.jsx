import React from 'react';
import { ArrowLeft, Download, Clock, ShieldCheck, ShieldAlert, Cpu, Layers } from 'lucide-react';
import RiskBadge from './RiskBadge';
import HeatmapOverlay from './HeatmapOverlay';
import FieldsTable from './FieldsTable';
import ForensicSignals from './ForensicSignals';

export default function DocumentResult({ result, onBack }) {
  if (!result) return null;

  const downloadReportJson = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(result, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `docshield_forensics_${result.doc_id}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Top Bar Navigation & Actions */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
        <button onClick={onBack} className="btn btn-secondary" style={{ padding: '8px 16px', fontSize: '0.82rem' }}>
          <ArrowLeft size={16} />
          Scan Another Document
        </button>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Clock size={14} />
            Latency: <strong style={{ color: '#ffffff', fontFamily: 'var(--font-mono)' }}>{result.processing_time_ms} ms</strong>
          </div>
          <button onClick={downloadReportJson} className="btn btn-secondary" style={{ padding: '8px 16px', fontSize: '0.82rem' }}>
            <Download size={15} />
            Export Forensics JSON
          </button>
        </div>
      </div>

      {/* Primary Risk Badge Verdict */}
      <RiskBadge
        score={result.risk_score}
        level={result.risk_level}
        isAuthentic={result.is_authentic}
      />

      {/* Executive Reason Banner */}
      <div className="glass-panel" style={{ padding: '18px 22px', borderLeft: result.is_authentic ? '4px solid var(--risk-low)' : '4px solid var(--risk-high)' }}>
        <div style={{ fontSize: '0.75rem', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: '4px' }}>
          Executive Forensic Assessment
        </div>
        <p style={{ fontSize: '0.92rem', color: '#ffffff', lineHeight: '1.5' }}>
          {result.summary_reason}
        </p>
      </div>

      {/* Interactive Visual Attention Heatmap & Bounding Boxes */}
      <HeatmapOverlay
        originalUrl={result.original_image_url}
        heatmapUrl={result.heatmap_url}
        forgerySignals={result.forgery_signals}
        docType={result.document_type}
      />

      {/* Extracted Structured Fields Table */}
      <FieldsTable fields={result.fields} />

      {/* Forensic Multi-Signal Detail Panel */}
      <ForensicSignals
        forgerySignals={result.forgery_signals}
        ruleChecks={result.rule_checks}
        modelVersions={result.model_versions}
      />
    </div>
  );
}
