import React from 'react';
import { Table, CheckCircle2, AlertOctagon, Info } from 'lucide-react';

export default function FieldsTable({ fields = [] }) {
  if (!fields || fields.length === 0) {
    return (
      <div className="glass-panel" style={{ padding: '20px', textAlign: 'center', color: 'var(--text-muted)' }}>
        No structured fields extracted.
      </div>
    );
  }

  return (
    <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '14px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <h3 style={{ fontSize: '1.05rem', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Table size={18} color="#38bdf8" />
          Extracted Document Fields & Anomaly Verification
        </h3>
        <span className="badge badge-indigo">
          {fields.length} Key-Value Entities
        </span>
      </div>

      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.85rem' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--border-subtle)', color: 'var(--text-muted)', fontSize: '0.75rem', textTransform: 'uppercase' }}>
              <th style={{ padding: '10px 12px' }}>Field Identifier</th>
              <th style={{ padding: '10px 12px' }}>Parsed Value</th>
              <th style={{ padding: '10px 12px' }}>OCR Confidence</th>
              <th style={{ padding: '10px 12px' }}>Forensic Status</th>
            </tr>
          </thead>
          <tbody>
            {fields.map((field, idx) => {
              const confPct = Math.round(field.confidence * 100);
              const isAnomaly = field.anomaly_flag;

              return (
                <tr
                  key={idx}
                  style={{
                    borderBottom: '1px solid var(--border-subtle)',
                    background: isAnomaly ? 'rgba(239, 68, 68, 0.08)' : 'transparent',
                    transition: 'background 0.15s ease'
                  }}
                >
                  {/* Field Name */}
                  <td style={{ padding: '12px', fontWeight: '600', color: 'var(--text-secondary)' }}>
                    {field.field_name.replace(/_/g, ' ').toUpperCase()}
                  </td>

                  {/* Value */}
                  <td style={{ padding: '12px', fontFamily: 'var(--font-mono)', fontWeight: '600', color: isAnomaly ? '#ef4444' : '#ffffff' }}>
                    {field.value}
                  </td>

                  {/* Confidence */}
                  <td style={{ padding: '12px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <div style={{ width: '50px', height: '6px', background: 'rgba(255,255,255,0.1)', borderRadius: '3px', overflow: 'hidden' }}>
                        <div style={{ width: `${confPct}%`, height: '100%', background: '#38bdf8' }} />
                      </div>
                      <span style={{ fontSize: '0.75rem', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
                        {confPct}%
                      </span>
                    </div>
                  </td>

                  {/* Anomaly Status */}
                  <td style={{ padding: '12px' }}>
                    {isAnomaly ? (
                      <div className="tooltip-container" style={{ cursor: 'help' }}>
                        <span className="badge badge-high" style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                          <AlertOctagon size={12} />
                          TAMPER FLAGGED
                          <Info size={11} style={{ opacity: 0.7 }} />
                        </span>
                        <span className="tooltip-text">
                          <strong>Forensic Anomaly:</strong> {field.anomaly_reason || 'Inconsistent typography or mathematical discrepancy.'}
                        </span>
                      </div>
                    ) : (
                      <span className="badge badge-low" style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                        <CheckCircle2 size={12} />
                        VERIFIED
                      </span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
