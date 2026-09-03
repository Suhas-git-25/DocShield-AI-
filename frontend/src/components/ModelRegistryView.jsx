import React, { useState } from 'react';
import { Cpu, CheckCircle2, RefreshCw, Sliders, Shield, ArrowRight, Layers } from 'lucide-react';

export default function ModelRegistryView({ models = [], onActivateModel, isActivating }) {
  const [selectedVersions, setSelectedVersions] = useState({});

  const handleVersionChange = (stage, version) => {
    setSelectedVersions(prev => ({ ...prev, [stage]: version }));
  };

  const handleActivate = (stage) => {
    const version = selectedVersions[stage];
    if (version) {
      onActivateModel(stage, version);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Header */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: '800', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Cpu size={22} color="#38bdf8" />
          Model Registry & Runtime Stage Activation
        </h2>
        <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: '4px' }}>
          Inspect versioned checkpoints for each pipeline stage and switch active models dynamically without redeploying.
        </p>
      </div>

      {/* Stages Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px' }}>
        {models.map((model) => {
          const selected = selectedVersions[model.stage] || model.active_version;
          const isCurrentActive = selected === model.active_version;

          return (
            <div key={model.stage} className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span style={{ fontSize: '0.75rem', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-muted)' }}>
                  Stage: {model.stage}
                </span>
                <span className="badge badge-low" style={{ fontSize: '0.65rem' }}>
                  ACTIVE: {model.active_version}
                </span>
              </div>

              <div>
                <h3 style={{ fontSize: '1.05rem', fontWeight: '700', color: '#ffffff', textTransform: 'capitalize' }}>
                  {model.stage} Module
                </h3>
                <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '4px', lineHeight: '1.4' }}>
                  {model.description}
                </p>
              </div>

              {/* Metrics Pills */}
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', background: 'rgba(0,0,0,0.25)', padding: '10px', borderRadius: '8px' }}>
                {Object.entries(model.metrics || {}).map(([mKey, mVal]) => (
                  <div key={mKey} style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                    {mKey.toUpperCase()}: <strong style={{ color: '#38bdf8', fontFamily: 'var(--font-mono)' }}>{mVal}</strong>
                  </div>
                ))}
              </div>

              {/* Version Selector & Activation Button */}
              <div style={{ marginTop: 'auto', display: 'flex', gap: '10px', alignItems: 'center' }}>
                <select
                  value={selected}
                  onChange={(e) => handleVersionChange(model.stage, e.target.value)}
                  style={{
                    flex: 1,
                    background: 'var(--bg-tertiary)',
                    color: '#ffffff',
                    border: '1px solid var(--border-subtle)',
                    borderRadius: '8px',
                    padding: '8px 10px',
                    fontSize: '0.8rem',
                    outline: 'none',
                    cursor: 'pointer'
                  }}
                >
                  {model.available_versions.map((ver) => (
                    <option key={ver} value={ver}>
                      {ver} {ver === model.active_version ? '(Currently Active)' : ''}
                    </option>
                  ))}
                </select>

                <button
                  onClick={() => handleActivate(model.stage)}
                  disabled={isCurrentActive || isActivating}
                  className="btn btn-primary"
                  style={{ padding: '8px 14px', fontSize: '0.78rem', whiteSpace: 'nowrap' }}
                >
                  {isCurrentActive ? (
                    'Active'
                  ) : (
                    'Promote'
                  )}
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
