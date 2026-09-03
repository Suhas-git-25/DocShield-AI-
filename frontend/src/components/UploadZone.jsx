import React, { useState } from 'react';
import { UploadCloud, FileText, CheckCircle2, Sparkles, RefreshCw, Zap, Shield, Image as ImageIcon } from 'lucide-react';

export default function UploadZone({ onAnalyze, isLoading, samples = [], onSelectSample }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [docTypeHint, setDocTypeHint] = useState('');
  const [isAsync, setIsAsync] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const [activeSampleKey, setActiveSampleKey] = useState(null);

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setSelectedFile(e.dataTransfer.files[0]);
      setActiveSampleKey(null);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
      setActiveSampleKey(null);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedFile && !activeSampleKey) return;
    onAnalyze({
      file: selectedFile,
      docTypeHint: docTypeHint || null,
      isAsync,
      sampleKey: activeSampleKey
    });
  };

  const handleSampleClick = async (sample) => {
    setActiveSampleKey(sample.filename.replace('.png', ''));
    setDocTypeHint(sample.document_type);

    try {
      // Fetch sample blob
      const res = await fetch(`/v1/documents/samples/file/${sample.filename}`);
      const blob = await res.blob();
      const file = new File([blob], sample.filename, { type: 'image/png' });
      setSelectedFile(file);
    } catch (err) {
      console.error('Failed to load sample blob:', err);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Upload Box */}
      <form onSubmit={handleSubmit} className="glass-panel" style={{ padding: '28px' }}>
        <div style={{ marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '12px' }}>
          <div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: '800', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <UploadCloud size={22} color="#38bdf8" />
              Upload Document for Forensic Inspection
            </h2>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: '4px' }}>
              Accepts IDs, Passports, Invoices, and Paystubs in PNG, JPEG, or PDF formats.
            </p>
          </div>

          {/* Doc Type Hint & Async Mode Controls */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
            <div>
              <select
                value={docTypeHint}
                onChange={(e) => setDocTypeHint(e.target.value)}
                style={{
                  background: 'var(--bg-tertiary)',
                  color: 'var(--text-primary)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '8px',
                  padding: '8px 12px',
                  fontSize: '0.8rem',
                  cursor: 'pointer',
                  outline: 'none'
                }}
              >
                <option value="">Auto-Detect Doc Type</option>
                <option value="id_card">National ID Card</option>
                <option value="passport">Passport Biodata</option>
                <option value="invoice">Business Invoice</option>
                <option value="paystub">Earnings / Paystub</option>
              </select>
            </div>

            <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem', color: 'var(--text-secondary)', cursor: 'pointer', background: 'var(--bg-tertiary)', padding: '6px 10px', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
              <input
                type="checkbox"
                checked={isAsync}
                onChange={(e) => setIsAsync(e.target.checked)}
                style={{ accentColor: '#38bdf8' }}
              />
              <Zap size={14} color={isAsync ? '#38bdf8' : 'var(--text-muted)'} />
              Async Queue
            </label>
          </div>
        </div>

        {/* Drag & Drop Area */}
        <div
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          style={{
            border: dragOver ? '2px dashed #38bdf8' : '2px dashed var(--border-subtle)',
            borderRadius: '14px',
            padding: '36px 20px',
            textAlign: 'center',
            background: dragOver ? 'rgba(56, 189, 248, 0.06)' : 'rgba(0,0,0,0.2)',
            cursor: 'pointer',
            transition: 'all 0.2s ease',
            position: 'relative'
          }}
          onClick={() => document.getElementById('file-upload-input').click()}
        >
          <input
            id="file-upload-input"
            type="file"
            accept="image/*,application/pdf"
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />

          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '56px',
              height: '56px',
              borderRadius: '16px',
              background: 'var(--bg-tertiary)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              border: '1px solid var(--border-subtle)'
            }}>
              {selectedFile ? (
                <FileText size={28} color="#38bdf8" />
              ) : (
                <UploadCloud size={28} color="var(--text-muted)" />
              )}
            </div>

            <div>
              {selectedFile ? (
                <div>
                  <div style={{ fontSize: '0.95rem', fontWeight: '700', color: '#ffffff' }}>
                    {selectedFile.name}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                    {(selectedFile.size / 1024).toFixed(1)} KB • Ready to analyze
                  </div>
                </div>
              ) : (
                <div>
                  <div style={{ fontSize: '0.95rem', fontWeight: '600', color: 'var(--text-primary)' }}>
                    Drag & drop document image or PDF here, or <span style={{ color: '#38bdf8' }}>browse</span>
                  </div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                    Supported: PNG, JPEG, PDF, TIFF, WebP (up to 15MB)
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Action Button */}
        <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'flex-end' }}>
          <button
            type="submit"
            disabled={!selectedFile || isLoading}
            className="btn btn-primary"
            style={{ padding: '12px 28px', fontSize: '0.92rem' }}
          >
            {isLoading ? (
              <>
                <RefreshCw size={18} className="animate-spin" />
                Executing Forensics Pipeline...
              </>
            ) : (
              <>
                <Shield size={18} />
                Analyze Document
              </>
            )}
          </button>
        </div>
      </form>

      {/* 1-Click Demo Samples Showcase */}
      {samples.length > 0 && (
        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
            <Sparkles size={18} color="#f59e0b" />
            <h3 style={{ fontSize: '1rem', fontWeight: '700' }}>
              Instant 1-Click Test Documents (Authentic & Forged Benchmarks)
            </h3>
          </div>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '16px' }}>
            Select any pre-packaged test document below to immediately inspect detection behavior across authentic samples and the 6 attack types:
          </p>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(230px, 1fr))',
            gap: '12px'
          }}>
            {samples.map((s, idx) => {
              const isSelected = activeSampleKey === s.filename.replace('.png', '');
              return (
                <div
                  key={idx}
                  onClick={() => handleSampleClick(s)}
                  style={{
                    background: isSelected ? 'rgba(56, 189, 248, 0.12)' : 'var(--bg-tertiary)',
                    border: isSelected ? '1px solid #38bdf8' : '1px solid var(--border-subtle)',
                    borderRadius: '10px',
                    padding: '12px 14px',
                    cursor: 'pointer',
                    transition: 'all 0.15s ease',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '6px'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <span style={{ fontSize: '0.8rem', fontWeight: '700', textTransform: 'capitalize', color: '#ffffff' }}>
                      {s.filename.replace('.png', '').replace(/_/g, ' ')}
                    </span>
                    {s.is_authentic ? (
                      <span className="badge badge-low" style={{ fontSize: '0.65rem' }}>Clean</span>
                    ) : (
                      <span className="badge badge-high" style={{ fontSize: '0.65rem' }}>{s.attack_type}</span>
                    )}
                  </div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'capitalize' }}>
                    Type: {s.document_type}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
