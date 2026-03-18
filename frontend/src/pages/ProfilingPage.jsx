import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { BarChart2, AlertTriangle, TrendingUp, Shield, ChevronRight } from 'lucide-react'
import { motion } from 'framer-motion'
import { RadialBarChart, RadialBar, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell } from 'recharts'
import { getProfile } from '../services/api'
import Spinner from '../components/ui/Spinner'
import Badge from '../components/ui/Badge'
import StatCard from '../components/ui/StatCard'

const DQIGauge = ({ score, grade }) => {
  const color = score >= 75 ? '#34d399' : score >= 50 ? '#fbbf24' : '#f87171'
  const data = [{ value: score, fill: color }]
  return (
    <div className="card-glow p-6 flex flex-col items-center">
      <p className="label mb-4">Data Quality Index</p>
      <div className="relative w-44 h-44">
        <ResponsiveContainer width="100%" height="100%">
          <RadialBarChart cx="50%" cy="50%" innerRadius="70%" outerRadius="90%" data={data} startAngle={220} endAngle={-40}>
            <RadialBar dataKey="value" cornerRadius={6} background={{ fill: '#1a2235' }} />
          </RadialBarChart>
        </ResponsiveContainer>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="font-display text-4xl font-800 text-white">{score?.toFixed(0)}</span>
          <span className="text-xs font-mono text-slate-500 mt-0.5">/ 100</span>
          <span className="font-display text-lg font-600 mt-1" style={{ color }}>{grade}</span>
        </div>
      </div>
    </div>
  )
}

const MissingChart = ({ missing }) => {
  const data = Object.entries(missing || {})
    .filter(([, v]) => v.missing_pct > 0)
    .sort((a, b) => b[1].missing_pct - a[1].missing_pct)
    .slice(0, 10)
    .map(([col, v]) => ({ col: col.length > 12 ? col.slice(0, 12) + '…' : col, pct: v.missing_pct }))

  if (!data.length) return (
    <div className="flex items-center justify-center h-32 text-slate-500 text-sm">
      ✓ No missing values detected
    </div>
  )

  return (
    <ResponsiveContainer width="100%" height={200}>
      <BarChart data={data} layout="vertical" margin={{ left: 10, right: 20 }}>
        <XAxis type="number" domain={[0, 100]} tick={{ fill: '#64748b', fontSize: 11, fontFamily: 'JetBrains Mono' }} tickFormatter={v => `${v}%`} />
        <YAxis type="category" dataKey="col" tick={{ fill: '#94a3b8', fontSize: 11 }} width={90} />
        <Tooltip formatter={(v) => [`${v}%`, 'Missing']} contentStyle={{ background: '#0a0f1e', border: '1px solid rgba(251,191,36,0.2)', borderRadius: 8, fontSize: 12 }} />
        <Bar dataKey="pct" radius={[0, 4, 4, 0]}>
          {data.map((d, i) => (
            <Cell key={i} fill={d.pct > 30 ? '#f87171' : d.pct > 10 ? '#fbbf24' : '#22d3ee'} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}

export default function ProfilingPage() {
  const { datasetId } = useParams()
  const navigate = useNavigate()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getProfile(datasetId)
      .then(r => setData(r.data))
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [datasetId])

  if (loading) return (
    <div className="flex items-center justify-center h-64 gap-3 text-slate-400">
      <Spinner /> <span className="font-mono text-sm">Running profiling pipeline…</span>
    </div>
  )

  if (error) return (
    <div className="flex items-center gap-3 text-red-400 p-6 card border-red-500/20 max-w-lg">
      <AlertTriangle size={18} /> <span className="text-sm">{error}</span>
    </div>
  )

  const { dqi, missing, outliers, correlation } = data
  const missingCols = Object.values(missing || {}).filter(v => v.missing_count > 0).length
  const outlierCols = Object.keys(outliers || {}).length
  const strongPairs = correlation?.strong_pairs?.length || 0

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-display text-2xl font-700 text-white">Profiling Report</h1>
          <p className="text-slate-500 text-sm font-mono mt-1">{datasetId}</p>
        </div>
        <button onClick={() => navigate(`/insights/${datasetId}`)} className="btn-primary flex items-center gap-2">
          View Insights <ChevronRight size={15} />
        </button>
      </div>

      {/* DQI + Stats */}
      <div className="grid grid-cols-4 gap-4">
        <DQIGauge score={dqi?.score} grade={dqi?.grade} />
        <StatCard label="Completeness" value={`${dqi?.completeness}%`} icon={Shield} />
        <StatCard label="Uniqueness" value={`${dqi?.uniqueness}%`} icon={TrendingUp} />
        <StatCard label="Outlier Score" value={`${dqi?.outlier_score}%`} icon={BarChart2} />
      </div>

      {/* Summary row */}
      <div className="grid grid-cols-3 gap-4">
        <StatCard label="Columns with Missing" value={missingCols} sub="columns affected" accent={missingCols > 0} />
        <StatCard label="Columns with Outliers" value={outlierCols} sub="numeric columns" accent={outlierCols > 0} />
        <StatCard label="Strong Correlations" value={strongPairs} sub="pairs ≥ 0.7" />
      </div>

      {/* Missing values chart */}
      <div className="card p-5">
        <p className="section-title mb-4">Missing Value Distribution</p>
        <MissingChart missing={missing} />
      </div>

      {/* Outliers table */}
      {outlierCols > 0 && (
        <div className="card p-5">
          <p className="section-title mb-4">Outlier Detection (IQR Method)</p>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-700/50">
                  {['Column', 'Outlier Count', 'Outlier %', 'Lower Bound', 'Upper Bound'].map(h => (
                    <th key={h} className="text-left text-xs font-mono text-slate-500 uppercase pb-3 pr-6">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {Object.entries(outliers).map(([col, v]) => (
                  <tr key={col} className="border-b border-slate-800 hover:bg-slate-800/30 transition-colors">
                    <td className="py-3 pr-6 font-mono text-slate-300">{col}</td>
                    <td className="py-3 pr-6 text-amber-400 font-mono">{v.outlier_count}</td>
                    <td className="py-3 pr-6">
                      <Badge label={`${v.outlier_pct}%`} variant={v.outlier_pct > 10 ? 'high' : 'medium'} />
                    </td>
                    <td className="py-3 pr-6 font-mono text-slate-400">{v.lower_bound}</td>
                    <td className="py-3 font-mono text-slate-400">{v.upper_bound}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Correlation pairs */}
      {strongPairs > 0 && (
        <div className="card p-5">
          <p className="section-title mb-4">Strong Correlations</p>
          <div className="space-y-2">
            {correlation.strong_pairs.map((p, i) => (
              <div key={i} className="flex items-center gap-4 p-3 bg-slate-800/30 rounded-lg">
                <span className="font-mono text-slate-300 text-sm">{p.col_a}</span>
                <div className="flex-1 h-1.5 bg-slate-700 rounded-full overflow-hidden">
                  <div className="h-full bg-amber-400 rounded-full" style={{ width: `${Math.abs(p.correlation) * 100}%` }} />
                </div>
                <span className="font-mono text-slate-300 text-sm">{p.col_b}</span>
                <Badge label={p.correlation.toFixed(3)} variant={p.correlation > 0 ? 'success' : 'warning'} />
              </div>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  )
}
