import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import UploadZone from './components/UploadZone';
import DocumentResult from './components/DocumentResult';
import AnalyticsDashboard from './components/AnalyticsDashboard';
import DocumentHistory from './components/DocumentHistory';
import ModelRegistryView from './components/ModelRegistryView';
import LandingShowcase from './components/LandingShowcase';

import {
  checkHealth,
  fetchSamples,
  analyzeDocumentSync,
  analyzeDocumentAsync,
  pollJobStatus,
  fetchDocumentHistory,
  fetchRobustnessReport,
  triggerBenchmark,
  fetchModels,
  activateModelVersion
} from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('scanner');
  const [systemHealth, setSystemHealth] = useState('healthy');
  const [samples, setSamples] = useState([]);
  const [history, setHistory] = useState([]);
  const [robustnessReport, setRobustnessReport] = useState(null);
  const [models, setModels] = useState([]);
  const [activeModelName, setActiveModelName] = useState('ViT-Adversarial');

  const [currentResult, setCurrentResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isBenchmarking, setIsBenchmarking] = useState(false);
  const [isActivating, setIsActivating] = useState(false);
  const [notification, setNotification] = useState(null);

  // Show Toast Notification
  const showToast = (message, type = 'info') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 4000);
  };

  // Initial Data Fetch
  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      const health = await checkHealth().catch(() => ({ status: 'degraded' }));
      setSystemHealth(health.status);

      const [samplesData, historyData, reportData, modelsData] = await Promise.all([
        fetchSamples().catch(() => []),
        fetchDocumentHistory().catch(() => []),
        fetchRobustnessReport().catch(() => null),
        fetchModels().catch(() => [])
      ]);

      setSamples(samplesData);
      setHistory(historyData);
      setRobustnessReport(reportData);
      setModels(modelsData);

      const forgeryStage = modelsData.find(m => m.stage === 'forgery');
      if (forgeryStage) {
        setActiveModelName(forgeryStage.active_version);
      }
    } catch (err) {
      console.error('Error during initial load:', err);
    }
  };

  // Document Analysis Handler (Sync & Async)
  const handleAnalyze = async ({ file, docTypeHint, isAsync, sampleKey }) => {
    setIsLoading(true);
    setCurrentResult(null);

    const formData = new FormData();
    formData.append('file', file);
    if (docTypeHint) formData.append('document_type_hint', docTypeHint);
    if (sampleKey) formData.append('sample_key', sampleKey);

    try {
      if (isAsync) {
        showToast('Enqueued job in async queue. Polling for results...', 'info');
        const job = await analyzeDocumentAsync(formData);
        
        // Poll for completion
        let attempts = 0;
        const pollInterval = setInterval(async () => {
          attempts++;
          try {
            const status = await pollJobStatus(job.job_id);
            if (status.status === 'completed' && status.result) {
              clearInterval(pollInterval);
              setIsLoading(false);
              setCurrentResult(status.result);
              setHistory(prev => [status.result, ...prev]);
              showToast('Async analysis complete!', 'success');
            } else if (status.status === 'failed') {
              clearInterval(pollInterval);
              setIsLoading(false);
              showToast(status.error || 'Job failed', 'error');
            } else if (attempts > 30) {
              clearInterval(pollInterval);
              setIsLoading(false);
              showToast('Job polling timed out', 'error');
            }
          } catch (e) {
            clearInterval(pollInterval);
            setIsLoading(false);
            showToast('Failed to poll job status', 'error');
          }
        }, 800);
      } else {
        const result = await analyzeDocumentSync(formData);
        setIsLoading(false);
        setCurrentResult(result);
        setHistory(prev => [result, ...prev]);
        showToast('Document analysis complete!', 'success');
      }
    } catch (err) {
      setIsLoading(false);
      showToast(err.message || 'Analysis failed', 'error');
    }
  };

  // Run On-Demand Benchmark Suite
  const handleTriggerBenchmark = async () => {
    setIsBenchmarking(true);
    try {
      showToast('Running dynamic adversarial robustness evaluation across all attack types...', 'info');
      await triggerBenchmark();
      const report = await fetchRobustnessReport();
      setRobustnessReport(report);
      setIsBenchmarking(false);
      showToast('Benchmark run complete! Metrics updated.', 'success');
    } catch (err) {
      setIsBenchmarking(false);
      showToast('Benchmark execution failed: ' + err.message, 'error');
    }
  };

  // Activate Model Version
  const handleActivateModel = async (stage, version) => {
    setIsActivating(true);
    try {
      await activateModelVersion(stage, version);
      const updatedModels = await fetchModels();
      setModels(updatedModels);
      if (stage === 'forgery') {
        setActiveModelName(version);
      }
      setIsActivating(false);
      showToast(`Activated ${stage} model version ${version}`, 'success');
    } catch (err) {
      setIsActivating(false);
      showToast('Model activation failed: ' + err.message, 'error');
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        systemHealth={systemHealth}
        activeModelVersion={activeModelName}
      />

      {/* Notification Toast */}
      {notification && (
        <div style={{
          position: 'fixed',
          bottom: '24px',
          right: '24px',
          zIndex: 1000,
          background: notification.type === 'error' ? 'var(--risk-high-bg)' : 'var(--bg-tertiary)',
          border: notification.type === 'error' ? '1px solid var(--risk-high-border)' : '1px solid var(--border-accent)',
          borderRadius: '10px',
          padding: '12px 20px',
          color: notification.type === 'error' ? 'var(--risk-high)' : '#38bdf8',
          boxShadow: '0 10px 25px rgba(0,0,0,0.6)',
          fontSize: '0.85rem',
          fontWeight: '600',
          backdropFilter: 'blur(10px)'
        }}>
          {notification.message}
        </div>
      )}

      {/* Main Content Area */}
      <main style={{ flex: 1, padding: '32px 0' }}>
        <div className="container">
          {activeTab === 'scanner' && (
            currentResult ? (
              <DocumentResult
                result={currentResult}
                onBack={() => setCurrentResult(null)}
              />
            ) : (
              <UploadZone
                onAnalyze={handleAnalyze}
                isLoading={isLoading}
                samples={samples}
              />
            )
          )}

          {activeTab === 'analytics' && (
            <AnalyticsDashboard
              report={robustnessReport}
              onTriggerBenchmark={handleTriggerBenchmark}
              isBenchmarking={isBenchmarking}
            />
          )}

          {activeTab === 'history' && (
            <DocumentHistory
              history={history}
              onSelectDocument={(doc) => {
                setCurrentResult(doc);
                setActiveTab('scanner');
              }}
            />
          )}

          {activeTab === 'models' && (
            <ModelRegistryView
              models={models}
              onActivateModel={handleActivateModel}
              isActivating={isActivating}
            />
          )}

          {activeTab === 'architecture' && (
            <LandingShowcase
              onStartScan={() => setActiveTab('scanner')}
            />
          )}
        </div>
      </main>

      {/* Footer */}
      <footer style={{
        borderTop: '1px solid var(--border-subtle)',
        padding: '24px 0',
        background: 'rgba(10, 13, 20, 0.6)',
        fontSize: '0.78rem',
        color: 'var(--text-muted)'
      }}>
        <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px' }}>
          <div>
            <strong>DocShield AI</strong> — Document Fraud Detection & Forensics Platform
          </div>
          <div style={{ display: 'flex', gap: '16px' }}>
            <span>Stack: Python 3.13 • PyTorch • FastAPI • React • Docker</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
