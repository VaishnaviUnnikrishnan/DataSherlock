import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Lightbulb, AlertTriangle, Sparkles, Wrench, ChevronRight, Info } from 'lucide-react'
import { motion } from 'framer-motion'
import { getInsights } from '../services/api'
import Spinner from '../components/ui/Spinner'
import Badge from '../components/ui/Badge'

const severityIcon = { warning: '⚠️', info: 'ℹ️', error: '🔴' }

function InsightCard({ item, index }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05 }}
      className="card p-4 hover:border-slate-600 transition-colors"
    >
      <div className="flex items-start gap-3">
        <span className="text-lg mt-0.5">{severityIcon[item.severity] || 'ℹ️'}</span>
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <span className="font-mono text-amber-400 text-xs">{item.column}</span>
            <Badge label={item.rule || item.finding || 'insight'} variant={item.severity === 'warning' ? 'warning' : 'info'} />
          </div>
          <p className="text-sm text-slate-300">{item.message || item.description}</p>
          {item.suggested_action && (
            <p className="text-xs font-mono text-cyan-400 mt-2 bg-cyan-400/5 px-2 py-1 rounded border border-cyan-400/10 inline-block">
              → {item.suggested_action}
            </p>
          )}
        </div>
      </div>
    </motion.div>
  )
}

function FeatureCard({ item, index }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05 }}
      className="card p-4"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <span className="font-mono text-xs text-slate-400">{item.source_column}</span>
            <span className="text-slate-600">→</span>
            <Badge label={item.suggestion} variant="info" />
          </div>
          <p className="text-sm text-slate-300 mb-2">{item.description}</p>
          <div className="flex flex-wrap gap-1">
            {item.new_features?.map(f => (
              <span key={f} className="tag bg-ink-950 text-emerald-400 border border-emerald-500/20">{f}</span>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  )
}

export default function InsightsPage() {
  const { datasetId } = useParams()
  const navigate = useNavigate()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [tab, setTab] = useState('rules')

  useEffect(() => {
    getInsights(datasetId)
      .then(r => setData(r.data))
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [datasetId])

  if (loading) return (
    <div className="flex items-center justify-center h-64 gap-3 text-slate-400">
      <Spinner /> <span className="font-mono text-sm">Generating insights…</span>
    </div>
  )

  if (error) return (
    <div className="flex items-center gap-3 text-red-400 p-6 card border-red-500/20 max-w-lg">
      <AlertTriangle size={18} /> <span className="text-sm">{error}</span>
    </div>
  )

  const tabs = [
    { key: 'rules', label: 'Rule Insights', icon: AlertTriangle, count: data?.rule_insights?.length },
    { key: 'root', label: 'Root Causes', icon: Info, count: data?.root_causes?.length },
    { key: 'features', label: 'Feature Suggestions', icon: Sparkles, count: data?.feature_suggestions?.length },
  ]

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-display text-2xl font-700 text-white">Insights</h1>
          <p className="text-slate-500 text-sm font-mono mt-1">{datasetId}</p>
        </div>
        <button onClick={() => navigate(`/ask/${datasetId}`)} className="btn-primary flex items-center gap-2">
          Ask AI <ChevronRight size={15} />
        </button>
      </div>

      {/* Summary cards */}
      <div className="grid grid-cols-3 gap-4">
        {tabs.map(t => (
          <button key={t.key} onClick={() => setTab(t.key)}
            className={`card p-4 text-left transition-all ${tab === t.key ? 'border-amber-400/30 bg-amber-400/5' : 'hover:border-slate-600'}`}>
            <div className="flex items-center gap-2 mb-2">
              <t.icon size={14} className={tab === t.key ? 'text-amber-400' : 'text-slate-500'} />
              <span className="label">{t.label}</span>
            </div>
            <span className={`font-display text-2xl font-700 ${tab === t.key ? 'text-amber-400' : 'text-white'}`}>{t.count}</span>
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div className="space-y-3">
        {tab === 'rules' && (
          data.rule_insights.length ? data.rule_insights.map((item, i) => <InsightCard key={i} item={item} index={i} />) :
          <div className="text-center py-12 text-slate-500 text-sm">✓ No rule violations detected</div>
        )}
        {tab === 'root' && (
          data.root_causes.length ? data.root_causes.map((item, i) => <InsightCard key={i} item={item} index={i} />) :
          <div className="text-center py-12 text-slate-500 text-sm">✓ No root cause issues detected</div>
        )}
        {tab === 'features' && (
          data.feature_suggestions.length ? data.feature_suggestions.map((item, i) => <FeatureCard key={i} item={item} index={i} />) :
          <div className="text-center py-12 text-slate-500 text-sm">No feature suggestions available</div>
        )}
      </div>
    </motion.div>
  )
}
