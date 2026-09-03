/**
 * DocShield AI - Frontend API Service Client
 */

const API_BASE = '/v1';

export async function checkHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('Health check failed');
  return res.json();
}

export async function fetchSamples() {
  const res = await fetch(`${API_BASE}/documents/samples`);
  if (!res.ok) throw new Error('Failed to fetch samples');
  return res.json();
}

export async function analyzeDocumentSync(formData) {
  const res = await fetch(`${API_BASE}/documents/analyze`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Analysis failed' }));
    throw new Error(err.detail || 'Analysis failed');
  }
  return res.json();
}

export async function analyzeDocumentAsync(formData) {
  const res = await fetch(`${API_BASE}/documents/analyze/async`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Async enqueue failed' }));
    throw new Error(err.detail || 'Async enqueue failed');
  }
  return res.json();
}

export async function pollJobStatus(jobId) {
  const res = await fetch(`${API_BASE}/documents/jobs/${jobId}`);
  if (!res.ok) throw new Error('Failed to query job status');
  return res.json();
}

export async function fetchDocumentHistory() {
  const res = await fetch(`${API_BASE}/documents/history`);
  if (!res.ok) throw new Error('Failed to fetch document history');
  return res.json();
}

export async function fetchRobustnessReport() {
  const res = await fetch(`${API_BASE}/eval/robustness-report`);
  if (!res.ok) throw new Error('Failed to fetch robustness report');
  return res.json();
}

export async function triggerBenchmark() {
  const res = await fetch(`${API_BASE}/eval/run-benchmark`, {
    method: 'POST',
  });
  if (!res.ok) throw new Error('Failed to execute benchmark');
  return res.json();
}

export async function fetchModels() {
  const res = await fetch(`${API_BASE}/models`);
  if (!res.ok) throw new Error('Failed to fetch model stages');
  return res.json();
}

export async function activateModelVersion(stage, version) {
  const res = await fetch(`${API_BASE}/models/${stage}/activate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ version }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Activation failed' }));
    throw new Error(err.detail || 'Activation failed');
  }
  return res.json();
}
