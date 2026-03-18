import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { LayoutDashboard, ExternalLink, BarChart2, TrendingUp, PieChart, ScatterChart, AlertTriangle } from 'lucide-react'
import { motion } from 'framer-motion'
import { generateDashboard } from '../services/api'
import Spinner from '../components/ui/Spinner'
import Badge from '../components/ui/Badge'

const chartIcons = {
  bar: BarChart2,
  line: TrendingUp,
  histogram: BarChart2,
  scatter: ScatterChart,
  pie: PieChart,
}

function ChartCard({ chart, index }) {
  const Icon = chartIcons[chart.type] || BarChart2
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.97 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: index * 0.06 }}
      className="card p-5 hover:border-slate-600 transition-colors"
    >
      <div className="flex items-start gap-3">
        <div className="p-2 bg-amber-400/10 border border-amber-400/20 rounded-lg">
          <Icon size={16} className="text-amber-400" />
        </div>
        <div className="flex-1">
          <p className="font-display text-white text-sm font-600 mb-1">{chart.title}</p>
          <div className="flex items-center gap-2 flex-wrap">
            <Badge label={chart.type} variant="info" />
            {chart.x && <span className="text-xs font-mono text-slate-500">x: {chart.x}</span>}
            {chart.y && <span className="text-xs font-mono text-slate-500">y: {chart.y}</span>}
          </div>
        </div>
      </div>
      {/* Placeholder visualization bar */}
      <div className="mt-4 h-20 bg-ink-950/50 rounded-lg flex items-end gap-1 px-3 pb-3 overflow-hidden">
        {Array.from({ length: 12 }, (_, i) => (
          <div key={i} className="flex-1 bg-amber-400/20 rounded-t" style={{ height: `${20 + Math.random() * 60}%`, opacity: 0.5 + (i % 3) * 0.2 }} />
        ))}
      </div>
    </motion.div>
  )
}

export default function DashboardPage() {
  const { datasetId } = useParams()
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleGenerate = async () => {
    setLoading(true)
    setError(null)
    try {
      const { data } = await generateDashboard(datasetId)
      setResult(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-display text-2xl font-700 text-white">Dashboard Generation</h1>
          <p className="text-slate-500 text-sm font-mono mt-1">{datasetId}</p>
        </div>
        {result?.dashboard_url && result.dashboard_url !== `/api/v1/dashboard/${datasetId}/local` && (
          <a href={result.dashboard_url} target="_blank" rel="noreferrer" className="btn-primary flex items-center gap-2">
            Open in Superset <ExternalLink size={14} />
          </a>
        )}
      </div>

      {!result ? (
        <div className="card-glow p-12 text-center">
          <div className="w-16 h-16 rounded-2xl bg-amber-400/10 border border-amber-400/20 flex items-center justify-center mx-auto mb-5">
            <LayoutDashboard size={28} className="text-amber-400" />
          </div>
          <h2 className="font-display text-white text-xl font-700 mb-2">Auto-Generate Dashboard</h2>
          <p className="text-slate-400 text-sm max-w-md mx-auto mb-6">
            DataSherlock will analyse your dataset and automatically select the most appropriate chart types, 
            then deploy them to Apache Superset.
          </p>
          <button onClick={handleGenerate} disabled={loading} className="btn-primary flex items-center gap-2 mx-auto disabled:opacity-40">
            {loading ? <><Spinner size={15} /> Generating…</> : <><LayoutDashboard size={15} /> Generate Dashboard</>}
          </button>
          {error && (
            <div className="mt-4 flex items-center gap-2 justify-center text-red-400 text-sm">
              <AlertTriangle size={14} /> {error}
            </div>
          )}
        </div>
      ) : (
        <>
          {/* Status */}
          <div className="card p-4 flex items-center gap-4">
            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <div>
              <p className="text-sm text-slate-300">
                Dashboard <Badge label={result.status} variant="success" /> via{' '}
                <span className="font-mono text-amber-400 text-xs">{result.source || 'local'}</span>
              </p>
            </div>
            <div className="ml-auto">
              <p className="label">Charts selected</p>
              <p className="font-display text-amber-400 text-lg font-700">{result.charts?.length}</p>
            </div>
          </div>

          {/* Chart specs */}
          <div>
            <p className="section-title mb-4">Selected Visualizations</p>
            <div className="grid grid-cols-2 gap-4">
              {result.charts?.map((chart, i) => <ChartCard key={i} chart={chart} index={i} />)}
            </div>
          </div>
        </>
      )}
    </motion.div>
  )
}
