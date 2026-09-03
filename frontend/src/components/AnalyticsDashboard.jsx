import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { BarChart3, TrendingUp, ShieldAlert, Cpu, Zap, RefreshCw, CheckCircle2, Award, ArrowUpRight } from 'lucide-react';

export default function AnalyticsDashboard({ report, onTriggerBenchmark, isBenchmarking }) {
  if (!report) {
    return (
      <div className="glass-panel" style={{ padding: '40px', textAlign: 'center' }}>
        <RefreshCw size={24} className="animate-spin" color="#38bdf8" style={{ margin: '0 auto 12px' }} />
        <p style={{ color: 'var(--text-muted)' }}>Loading adversarial robustness benchmark data...</p>
      </div>
    );
  }

  const { metrics_a, metrics_b, improvement_summary, recommendations } = report;

  // Prepare data for per-attack recall chart
  const attackTypes = Object.keys(metrics_b.per_attack_recall || {});
  const chartData = attackTypes.map((att) => ({
    name: att.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()),
    'Phase 1 Baseline (ViT)': Math.round((metrics_a.per_attack_recall[att] || 0) * 100),
    'Phase 2 Adversarially Retrained': Math.round((metrics_b.per_attack_recall[att] || 0) * 100),
  }));

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Header & Benchmark Trigger */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <h2 style={{ fontSize: '1.35rem', fontWeight: '800' }}>
              Adversarial Robustness & Benchmarking Dashboard
            </h2>
            <span className="badge badge-indigo">Empirical ML Evaluation</span>
          </div>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: '4px' }}>
            Comparing Phase 1 Baseline ViT vs. Phase 2 Adversarially Retrained Checkpoint against Easy, Medium, and Hard attacks.
          </p>
        </div>

        <button
          onClick={onTriggerBenchmark}
          disabled={isBenchmarking}
          className="btn btn-primary"
          style={{ padding: '10px 20px', fontSize: '0.85rem' }}
        >
          {isBenchmarking ? (
            <>
              <RefreshCw size={16} className="animate-spin" />
              Running Adversarial Suite...
            </>
          ) : (
            <>
              <Zap size={16} />
              Run On-Demand Benchmark
            </>
          )}
        </button>
      </div>

      {/* KPI Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
        <div className="glass-panel" style={{ padding: '20px', borderLeft: '4px solid #38bdf8' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: '600', color: 'var(--text-muted)', textTransform: 'uppercase' }}>
            AUROC Discrimination
          </div>
          <div style={{ fontSize: '1.6rem', fontWeight: '800', color: '#ffffff', marginTop: '6px', fontFamily: 'var(--font-mono)' }}>
            {(metrics_b.auroc * 100).toFixed(1)}%
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--risk-low)', display: 'flex', alignItems: 'center', gap: '4px', marginTop: '4px' }}>
            <ArrowUpRight size={14} />
            +{(improvement_summary.auroc_delta * 100).toFixed(1)}% over Phase 1 baseline
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px', borderLeft: '4px solid #6366f1' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: '600', color: 'var(--text-muted)', textTransform: 'uppercase' }}>
            F1-Score (All Attacks)
          </div>
          <div style={{ fontSize: '1.6rem', fontWeight: '800', color: '#ffffff', marginTop: '6px', fontFamily: 'var(--font-mono)' }}>
            {(metrics_b.f1_score * 100).toFixed(1)}%
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--risk-low)', display: 'flex', alignItems: 'center', gap: '4px', marginTop: '4px' }}>
            <ArrowUpRight size={14} />
            +{(improvement_summary.f1_score_delta * 100).toFixed(1)}% F1 improvement
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px', borderLeft: '4px solid #10b981' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: '600', color: 'var(--text-muted)', textTransform: 'uppercase' }}>
            Hard-Tier Accuracy
          </div>
          <div style={{ fontSize: '1.6rem', fontWeight: '800', color: '#ffffff', marginTop: '6px', fontFamily: 'var(--font-mono)' }}>
            {(metrics_b.tier_accuracy.hard * 100).toFixed(1)}%
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--risk-low)', display: 'flex', alignItems: 'center', gap: '4px', marginTop: '4px' }}>
            <ArrowUpRight size={14} />
            +{(improvement_summary.hard_tier_accuracy_gain * 100).toFixed(1)}% on hard attacks
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px', borderLeft: '4px solid #f59e0b' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: '600', color: 'var(--text-muted)', textTransform: 'uppercase' }}>
            Localization IoU
          </div>
          <div style={{ fontSize: '1.6rem', fontWeight: '800', color: '#ffffff', marginTop: '6px', fontFamily: 'var(--font-mono)' }}>
            {metrics_b.localization_iou.toFixed(3)}
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--risk-low)', display: 'flex', alignItems: 'center', gap: '4px', marginTop: '4px' }}>
            <ArrowUpRight size={14} />
            +{improvement_summary.localization_iou_gain} IoU gain
          </div>
        </div>
      </div>

      {/* Main Robustness Grouped Bar Chart */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
          <div>
            <h3 style={{ fontSize: '1.05rem', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <BarChart3 size={18} color="#38bdf8" />
              Per-Attack-Type Detection Recall (Phase 1 Baseline vs. Phase 2 Adversarial Retrained)
            </h3>
            <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
              Recall measures the percentage of tampered documents successfully flagged per attack category.
            </p>
          </div>
        </div>

        <div style={{ width: '100%', height: '360px' }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={chartData}
              margin={{ top: 20, right: 30, left: 0, bottom: 20 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
              <XAxis dataKey="name" stroke="#94a3b8" fontSize={12} tickLine={false} />
              <YAxis stroke="#94a3b8" fontSize={12} unit="%" domain={[40, 100]} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0a0d14',
                  borderColor: 'rgba(255,255,255,0.15)',
                  borderRadius: '8px',
                  boxShadow: '0 10px 25px rgba(0,0,0,0.5)',
                  fontSize: '0.8rem',
                  fontFamily: 'var(--font-mono)'
                }}
              />
              <Legend wrapperStyle={{ paddingTop: '10px' }} />
              <Bar dataKey="Phase 1 Baseline (ViT)" fill="#64748b" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Phase 2 Adversarially Retrained" fill="#38bdf8" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Difficulty Tier Breakdown & Held-out Generalization */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        {/* Tier Cards */}
        <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <h3 style={{ fontSize: '1rem', fontWeight: '700' }}>
            Performance by Difficulty Tier
          </h3>

          {['easy', 'medium', 'hard'].map((tier) => {
            const accA = Math.round(metrics_a.tier_accuracy[tier] * 100);
            const accB = Math.round(metrics_b.tier_accuracy[tier] * 100);
            return (
              <div key={tier} style={{ background: 'var(--bg-tertiary)', padding: '12px 16px', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                  <span style={{ fontSize: '0.82rem', fontWeight: '700', textTransform: 'uppercase', color: '#ffffff' }}>
                    {tier} Tier
                  </span>
                  <span style={{ fontSize: '0.75rem', fontFamily: 'var(--font-mono)', color: '#38bdf8' }}>
                    Phase 1: {accA}% ➔ <strong style={{ color: 'var(--risk-low)' }}>Phase 2: {accB}%</strong>
                  </span>
                </div>
                <div style={{ height: '6px', background: 'rgba(255,255,255,0.1)', borderRadius: '3px', overflow: 'hidden' }}>
                  <div style={{ width: `${accB}%`, height: '100%', background: tier === 'hard' ? '#f59e0b' : '#38bdf8' }} />
                </div>
              </div>
            );
          })}
        </div>

        {/* Retraining Recommendations & Insights */}
        <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <h3 style={{ fontSize: '1rem', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Award size={18} color="#f59e0b" />
            Adversarial Retraining Findings & Deployment Decision
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {recommendations.map((rec, idx) => (
              <div key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '10px', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                <CheckCircle2 size={16} color="#10b981" style={{ flexShrink: 0, marginTop: '2px' }} />
                <span>{rec}</span>
              </div>
            ))}
          </div>

          <div style={{ marginTop: 'auto', background: 'rgba(56, 189, 248, 0.08)', border: '1px solid rgba(56, 189, 248, 0.25)', borderRadius: '8px', padding: '12px', fontSize: '0.78rem', color: '#38bdf8' }}>
            <strong>Active Production Model:</strong> ViT-Adversarial-Phase2 with attention rollout localization active.
          </div>
        </div>
      </div>
    </div>
  );
}
