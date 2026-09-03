import React from 'react';
import { ShieldCheck, AlertTriangle, ShieldAlert } from 'lucide-react';

export default function RiskBadge({ score, level, isAuthentic, size = 'normal' }) {
  const isHigh = level === 'high' || score >= 0.65;
  const isMed = level === 'medium' || (score >= 0.35 && score < 0.65);
  const isLow = level === 'low' || score < 0.35;

  let color = 'var(--risk-low)';
  let bg = 'var(--risk-low-bg)';
  let border = 'var(--risk-low-border)';
  let label = 'AUTHENTIC / LOW RISK';
  let Icon = ShieldCheck;

  if (isHigh) {
    color = 'var(--risk-high)';
    bg = 'var(--risk-high-bg)';
    border = 'var(--risk-high-border)';
    label = 'FORGERY DETECTED / HIGH RISK';
    Icon = ShieldAlert;
  } else if (isMed) {
    color = 'var(--risk-med)';
    bg = 'var(--risk-med-bg)';
    border = 'var(--risk-med-border)';
    label = 'SUSPICIOUS / MEDIUM RISK';
    Icon = AlertTriangle;
  }

  const percentage = Math.round(score * 100);

  if (size === 'compact') {
    return (
      <div style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '6px',
        padding: '3px 8px',
        borderRadius: '6px',
        background: bg,
        border: `1px solid ${border}`,
        color: color,
        fontSize: '0.75rem',
        fontWeight: '700',
        fontFamily: 'var(--font-mono)'
      }}>
        <Icon size={12} />
        <span>{percentage}%</span>
        <span>•</span>
        <span style={{ fontSize: '0.7rem', textTransform: 'uppercase' }}>{level}</span>
      </div>
    );
  }

  return (
    <div style={{
      background: bg,
      border: `1px solid ${border}`,
      borderRadius: '14px',
      padding: '16px 20px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: '16px',
      boxShadow: `0 0 20px ${bg}`
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        <div style={{
          width: '46px',
          height: '46px',
          borderRadius: '12px',
          background: color,
          color: '#ffffff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: `0 0 15px ${color}`
        }}>
          <Icon size={26} />
        </div>
        <div>
          <div style={{ fontSize: '0.75rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: color }}>
            {label}
          </div>
          <div style={{ fontSize: '1.25rem', fontWeight: '800', color: '#ffffff', display: 'flex', alignItems: 'baseline', gap: '6px' }}>
            <span>Fraud Risk Score:</span>
            <span style={{ color: color, fontFamily: 'var(--font-mono)' }}>{score.toFixed(3)}</span>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: '400' }}>({percentage}%)</span>
          </div>
        </div>
      </div>

      {/* Mini Visual Meter Bar */}
      <div style={{ width: '160px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: '4px', fontFamily: 'var(--font-mono)' }}>
          <span>0.0</span>
          <span>0.5</span>
          <span>1.0</span>
        </div>
        <div style={{ height: '8px', background: 'rgba(0,0,0,0.5)', borderRadius: '4px', overflow: 'hidden', border: '1px solid rgba(255,255,255,0.1)' }}>
          <div style={{
            height: '100%',
            width: `${percentage}%`,
            background: color,
            transition: 'width 0.8s ease'
          }} />
        </div>
      </div>
    </div>
  );
}
