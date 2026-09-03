import React, { useState } from 'react';
import { Eye, Layers, SplitSquareVertical, Sliders, Maximize2, ShieldAlert } from 'lucide-react';

export default function HeatmapOverlay({ originalUrl, heatmapUrl, forgerySignals = [], docType }) {
  const [viewMode, setViewMode] = useState('overlay'); // 'overlay', 'side-by-side', 'original', 'heatmap'
  const [opacity, setOpacity] = useState(0.65);
  const [showBBoxes, setShowBBoxes] = useState(true);

  return (
    <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
      {/* Header & Controls */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h3 style={{ fontSize: '1.05rem', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Eye size={18} color="#38bdf8" />
            Visual Forensics & Attention Heatmap
          </h3>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
            ViT transformer attention rollout + Error Level Analysis (ELA) spatial variance map
          </p>
        </div>

        {/* View Mode Switcher */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'var(--bg-tertiary)', padding: '4px', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
          <button
            onClick={() => setViewMode('overlay')}
            style={{
              padding: '6px 10px',
              borderRadius: '6px',
              fontSize: '0.75rem',
              fontWeight: '600',
              border: 'none',
              cursor: 'pointer',
              background: viewMode === 'overlay' ? '#38bdf8' : 'transparent',
              color: viewMode === 'overlay' ? '#0f172a' : 'var(--text-secondary)'
            }}
          >
            Overlay Blend
          </button>
          <button
            onClick={() => setViewMode('side-by-side')}
            style={{
              padding: '6px 10px',
              borderRadius: '6px',
              fontSize: '0.75rem',
              fontWeight: '600',
              border: 'none',
              cursor: 'pointer',
              background: viewMode === 'side-by-side' ? '#38bdf8' : 'transparent',
              color: viewMode === 'side-by-side' ? '#0f172a' : 'var(--text-secondary)'
            }}
          >
            Side-by-Side
          </button>
          <button
            onClick={() => setViewMode('original')}
            style={{
              padding: '6px 10px',
              borderRadius: '6px',
              fontSize: '0.75rem',
              fontWeight: '600',
              border: 'none',
              cursor: 'pointer',
              background: viewMode === 'original' ? '#38bdf8' : 'transparent',
              color: viewMode === 'original' ? '#0f172a' : 'var(--text-secondary)'
            }}
          >
            Original
          </button>
        </div>
      </div>

      {/* Opacity & Bounding Box Controls */}
      {viewMode === 'overlay' && (
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', background: 'rgba(0,0,0,0.25)', padding: '8px 14px', borderRadius: '8px', border: '1px solid var(--border-subtle)', fontSize: '0.78rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Sliders size={14} color="var(--text-muted)" />
            <span style={{ color: 'var(--text-secondary)' }}>Heatmap Intensity:</span>
            <input
              type="range"
              min="0.1"
              max="1.0"
              step="0.05"
              value={opacity}
              onChange={(e) => setOpacity(parseFloat(e.target.value))}
              style={{ width: '120px', accentColor: '#38bdf8', cursor: 'pointer' }}
            />
            <span style={{ fontFamily: 'var(--font-mono)', color: '#ffffff' }}>{Math.round(opacity * 100)}%</span>
          </div>

          <label style={{ display: 'flex', alignItems: 'center', gap: '6px', cursor: 'pointer', color: 'var(--text-secondary)' }}>
            <input
              type="checkbox"
              checked={showBBoxes}
              onChange={(e) => setShowBBoxes(e.target.checked)}
              style={{ accentColor: '#ef4444' }}
            />
            Highlight Tamper Bounding Boxes
          </label>
        </div>
      )}

      {/* Visual Canvas Display */}
      <div style={{
        background: '#030712',
        borderRadius: '12px',
        padding: '16px',
        border: '1px solid var(--border-subtle)',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '380px',
        overflow: 'hidden'
      }}>
        {viewMode === 'side-by-side' ? (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', width: '100%' }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '0.75rem', fontWeight: '600', color: 'var(--text-muted)', marginBottom: '8px' }}>
                ORIGINAL INGESTED DOCUMENT
              </div>
              <img
                src={originalUrl}
                alt="Original Document"
                style={{ maxWidth: '100%', maxHeight: '420px', borderRadius: '8px', objectFit: 'contain', border: '1px solid rgba(255,255,255,0.1)' }}
              />
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '0.75rem', fontWeight: '600', color: '#38bdf8', marginBottom: '8px' }}>
                ATTENTION / ELA HEATMAP
              </div>
              <img
                src={heatmapUrl}
                alt="Heatmap Overlay"
                style={{ maxWidth: '100%', maxHeight: '420px', borderRadius: '8px', objectFit: 'contain', border: '1px solid rgba(56,189,248,0.3)' }}
              />
            </div>
          </div>
        ) : viewMode === 'original' ? (
          <img
            src={originalUrl}
            alt="Original Document"
            style={{ maxWidth: '100%', maxHeight: '450px', borderRadius: '8px', objectFit: 'contain' }}
          />
        ) : (
          /* Overlay Mode */
          <div style={{ position: 'relative', display: 'inline-block', maxWidth: '100%' }}>
            <img
              src={originalUrl}
              alt="Base Document"
              style={{ maxWidth: '100%', maxHeight: '450px', borderRadius: '8px', objectFit: 'contain', display: 'block' }}
            />
            <img
              src={heatmapUrl}
              alt="Heatmap Overlay"
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                opacity: opacity,
                borderRadius: '8px',
                pointerEvents: 'none',
                mixBlendMode: 'screen',
                transition: 'opacity 0.15s ease'
              }}
            />

            {/* Tamper Bounding Boxes */}
            {showBBoxes && forgerySignals.map((sig, idx) => {
              if (!sig.region_bbox || sig.region_bbox.length !== 4) return null;
              const [x1, y1, x2, y2] = sig.region_bbox;
              const top = `${y1 * 100}%`;
              const left = `${x1 * 100}%`;
              const width = `${Math.max(2, (x2 - x1) * 100)}%`;
              const height = `${Math.max(2, (y2 - y1) * 100)}%`;

              return (
                <div
                  key={idx}
                  style={{
                    position: 'absolute',
                    top,
                    left,
                    width,
                    height,
                    border: '2px dashed #ef4444',
                    background: 'rgba(239, 68, 68, 0.25)',
                    borderRadius: '4px',
                    boxShadow: '0 0 12px rgba(239, 68, 68, 0.6)',
                    pointerEvents: 'auto'
                  }}
                  className="tooltip-container"
                >
                  <div style={{
                    position: 'absolute',
                    top: '-20px',
                    left: '0',
                    background: '#ef4444',
                    color: '#ffffff',
                    fontSize: '0.65rem',
                    fontWeight: '700',
                    padding: '1px 6px',
                    borderRadius: '3px',
                    whiteSpace: 'nowrap'
                  }}>
                    {sig.attack_type_guess || 'Tampered Region'}
                  </div>
                  <span className="tooltip-text">
                    <strong>{sig.attack_type_guess?.toUpperCase()}:</strong> {sig.description || 'High visual tampering anomaly detected.'}
                  </span>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Legend */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <div style={{ width: '12px', height: '12px', background: '#3b82f6', borderRadius: '3px' }} />
            <span>Low Activation / Base Pixel</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <div style={{ width: '12px', height: '12px', background: '#f59e0b', borderRadius: '3px' }} />
            <span>Medium Attention</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <div style={{ width: '12px', height: '12px', background: '#ef4444', borderRadius: '3px' }} />
            <span>High Forgery Discrepancy (Hotspot)</span>
          </div>
        </div>

        <div>
          Doc Type: <strong style={{ color: '#ffffff', textTransform: 'capitalize' }}>{docType}</strong>
        </div>
      </div>
    </div>
  );
}
