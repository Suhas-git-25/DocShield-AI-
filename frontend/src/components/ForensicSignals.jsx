import React from 'react';
import { ShieldCheck, ShieldAlert, Cpu, AlertTriangle, FileText, CheckCircle2, XCircle } from 'lucide-react';

export default function ForensicSignals({ forgerySignals = [], ruleChecks = [], modelVersions = {} }) {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
      {/* Visual Model Signals */}
      <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '14px' }}>
        <h3 style={{ fontSize: '1rem', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Cpu size={18} color="#38bdf8" />
          Neural Visual Forgery Model Signals
        </h3>

        {forgerySignals.length === 0 ? (
          <div style={{
            background: 'var(--risk-low-bg)',
            border: '1px solid var(--risk-low-border)',
            borderRadius: '10px',
            padding: '14px',
            display: 'flex',
            alignItems: 'center',
            gap: '12px'
          }}>
            <ShieldCheck size={22} color="var(--risk-low)" />
            <div>
              <div style={{ fontSize: '0.85rem', fontWeight: '700', color: 'var(--risk-low)' }}>
                Clean Pixel Statistics
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                No copy-move duplications, splicing artifacts, or ELA double-compression boundaries detected.
              </div>
            </div>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {forgerySignals.map((sig, idx) => (
              <div
                key={idx}
                style={{
                  background: 'var(--risk-high-bg)',
                  border: '1px solid var(--risk-high-border)',
                  borderRadius: '10px',
                  padding: '14px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '6px'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <ShieldAlert size={18} color="var(--risk-high)" />
                    <span style={{ fontWeight: '700', fontSize: '0.85rem', textTransform: 'uppercase', color: 'var(--risk-high)' }}>
                      {sig.attack_type_guess || 'Visual Forgery'}
                    </span>
                  </div>
                  <span className="badge badge-high" style={{ fontFamily: 'var(--font-mono)' }}>
                    Score: {(sig.anomaly_score * 100).toFixed(1)}%
                  </span>
                </div>
                <p style={{ fontSize: '0.78rem', color: 'var(--text-primary)', lineHeight: '1.4' }}>
                  {sig.description}
                </p>
                {sig.region_bbox && (
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                    BBox: [{sig.region_bbox.map(n => n.toFixed(3)).join(', ')}]
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Model Version Attribution */}
        <div style={{ marginTop: 'auto', paddingTop: '10px', borderTop: '1px solid var(--border-subtle)', display: 'flex', flexWrap: 'wrap', gap: '8px', fontSize: '0.72rem', color: 'var(--text-muted)' }}>
          <span>Active Pipeline Checkpoints:</span>
          {Object.entries(modelVersions).map(([stage, ver]) => (
            <span key={stage} style={{ fontFamily: 'var(--font-mono)', background: 'rgba(255,255,255,0.05)', padding: '2px 6px', borderRadius: '4px' }}>
              {stage}: <strong style={{ color: '#38bdf8' }}>{ver}</strong>
            </span>
          ))}
        </div>
      </div>

      {/* Deterministic Rule Engine Checks */}
      <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '14px' }}>
        <h3 style={{ fontSize: '1rem', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <FileText size={18} color="#6366f1" />
          Rule-Based & Metadata Forensics
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {ruleChecks.map((rule, idx) => {
            const passed = rule.passed;
            return (
              <div
                key={idx}
                style={{
                  background: passed ? 'rgba(255,255,255,0.03)' : 'var(--risk-high-bg)',
                  border: passed ? '1px solid var(--border-subtle)' : '1px solid var(--risk-high-border)',
                  borderRadius: '10px',
                  padding: '12px 14px',
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '10px'
                }}
              >
                {passed ? (
                  <CheckCircle2 size={18} color="var(--risk-low)" style={{ flexShrink: 0, marginTop: '2px' }} />
                ) : (
                  <XCircle size={18} color="var(--risk-high)" style={{ flexShrink: 0, marginTop: '2px' }} />
                )}
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '2px' }}>
                    <span style={{ fontSize: '0.82rem', fontWeight: '700', color: passed ? '#ffffff' : 'var(--risk-high)' }}>
                      {rule.check_name}
                    </span>
                    <span style={{ fontSize: '0.7rem', fontWeight: '600', textTransform: 'uppercase', color: passed ? 'var(--risk-low)' : 'var(--risk-high)' }}>
                      {passed ? 'PASSED' : 'VIOLATION'}
                    </span>
                  </div>
                  <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', lineHeight: '1.35' }}>
                    {rule.details}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
