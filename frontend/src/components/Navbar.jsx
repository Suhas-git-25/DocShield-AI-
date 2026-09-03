import React from 'react';
import { Shield, Activity, BarChart3, History, Cpu, FileCode2, Layers } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, systemHealth, activeModelVersion }) {
  const tabs = [
    { id: 'scanner', label: 'Document Scanner', icon: Shield },
    { id: 'analytics', label: 'Robustness Analytics', icon: BarChart3 },
    { id: 'history', label: 'Scan History', icon: History },
    { id: 'models', label: 'Model Registry', icon: Cpu },
    { id: 'architecture', label: 'Architecture & Spec', icon: Layers },
  ];

  return (
    <header style={{
      borderBottom: '1px solid var(--border-subtle)',
      background: 'rgba(10, 13, 20, 0.85)',
      backdropFilter: 'blur(12px)',
      position: 'sticky',
      top: 0,
      zIndex: 100
    }}>
      <div className="container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: '70px' }}>
        {/* Brand Logo */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', cursor: 'pointer' }} onClick={() => setActiveTab('scanner')}>
          <div style={{
            width: '42px',
            height: '42px',
            borderRadius: '12px',
            background: 'linear-gradient(135deg, #0284c7, #4f46e5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 0 20px rgba(14, 165, 233, 0.35)'
          }}>
            <Shield size={24} color="#ffffff" />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ fontSize: '1.25rem', fontWeight: '800', letterSpacing: '-0.02em', background: 'linear-gradient(to right, #ffffff, #94a3b8)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                DocShield AI
              </span>
              <span className="badge badge-cyan" style={{ fontSize: '0.65rem', padding: '2px 8px' }}>
                v1.0
              </span>
            </div>
            <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: '500' }}>
              Document Fraud Detection & Forensics
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  padding: '8px 14px',
                  borderRadius: '10px',
                  fontSize: '0.85rem',
                  fontWeight: isActive ? '600' : '500',
                  color: isActive ? '#ffffff' : 'var(--text-secondary)',
                  background: isActive ? 'var(--bg-tertiary)' : 'transparent',
                  border: isActive ? '1px solid var(--border-accent)' : '1px solid transparent',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
              >
                <Icon size={16} color={isActive ? '#38bdf8' : 'currentColor'} />
                {tab.label}
              </button>
            );
          })}
        </nav>

        {/* System & Model Status Pill */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            background: 'var(--bg-tertiary)',
            padding: '6px 12px',
            borderRadius: '10px',
            border: '1px solid var(--border-subtle)',
            fontSize: '0.78rem'
          }}>
            <div style={{
              width: '8px',
              height: '8px',
              borderRadius: '50%',
              background: systemHealth === 'healthy' ? '#10b981' : '#ef4444',
              boxShadow: systemHealth === 'healthy' ? '0 0 10px #10b981' : 'none'
            }} />
            <span style={{ color: 'var(--text-secondary)' }}>Engine:</span>
            <span style={{ color: '#ffffff', fontWeight: '600', fontFamily: 'var(--font-mono)', fontSize: '0.75rem' }}>
              {activeModelVersion || 'ViT-Adversarial'}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
}
