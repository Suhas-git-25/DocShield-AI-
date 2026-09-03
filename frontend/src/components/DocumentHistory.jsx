import React, { useState } from 'react';
import { History, Search, Filter, ShieldCheck, ShieldAlert, AlertTriangle, ArrowRight } from 'lucide-react';
import RiskBadge from './RiskBadge';

export default function DocumentHistory({ history = [], onSelectDocument }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterLevel, setFilterLevel] = useState('all');

  const filteredHistory = history.filter((item) => {
    const matchesSearch = item.doc_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          item.document_type.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          item.summary_reason.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterLevel === 'all' || item.risk_level === filterLevel;
    return matchesSearch && matchesFilter;
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Search & Filter Header */}
      <div className="glass-panel" style={{ padding: '20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h2 style={{ fontSize: '1.25rem', fontWeight: '800', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <History size={20} color="#38bdf8" />
            Document Verification History
          </h2>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
            Audit log of all analyzed documents with extracted signals and risk assessments.
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
          {/* Search Box */}
          <div style={{ position: 'relative', width: '220px' }}>
            <Search size={15} color="var(--text-muted)" style={{ position: 'absolute', left: '10px', top: '50%', transform: 'translateY(-50%)' }} />
            <input
              type="text"
              placeholder="Search by ID or type..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{
                width: '100%',
                background: 'var(--bg-tertiary)',
                border: '1px solid var(--border-subtle)',
                borderRadius: '8px',
                padding: '8px 12px 8px 32px',
                fontSize: '0.8rem',
                color: '#ffffff',
                outline: 'none'
              }}
            />
          </div>

          {/* Filter Level */}
          <div style={{ display: 'flex', gap: '6px' }}>
            {['all', 'low', 'medium', 'high'].map((lvl) => (
              <button
                key={lvl}
                onClick={() => setFilterLevel(lvl)}
                style={{
                  padding: '6px 12px',
                  borderRadius: '8px',
                  fontSize: '0.75rem',
                  fontWeight: '600',
                  border: 'none',
                  cursor: 'pointer',
                  textTransform: 'capitalize',
                  background: filterLevel === lvl ? '#38bdf8' : 'var(--bg-tertiary)',
                  color: filterLevel === lvl ? '#0f172a' : 'var(--text-secondary)'
                }}
              >
                {lvl}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* History Items List */}
      {filteredHistory.length === 0 ? (
        <div className="glass-panel" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
          No documents found matching the filter criteria.
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {filteredHistory.map((item) => (
            <div
              key={item.doc_id}
              className="glass-panel"
              style={{
                padding: '16px 20px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                flexWrap: 'wrap',
                gap: '16px',
                cursor: 'pointer',
                transition: 'all 0.15s ease'
              }}
              onClick={() => onSelectDocument(item)}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                <RiskBadge score={item.risk_score} level={item.risk_level} isAuthentic={item.is_authentic} size="compact" />

                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <strong style={{ fontSize: '0.95rem', color: '#ffffff', fontFamily: 'var(--font-mono)' }}>
                      #{item.doc_id}
                    </strong>
                    <span className="badge badge-indigo" style={{ fontSize: '0.65rem' }}>
                      {item.document_type}
                    </span>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                      {item.processing_time_ms} ms
                    </span>
                  </div>

                  <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '4px', maxWidth: '600px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {item.summary_reason}
                  </p>
                </div>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#38bdf8', fontSize: '0.82rem', fontWeight: '600' }}>
                <span>Inspect Forensics</span>
                <ArrowRight size={16} />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
