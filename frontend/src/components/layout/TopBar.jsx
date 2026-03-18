import { useLocation, useParams } from 'react-router-dom'
import { ChevronRight } from 'lucide-react'

const routeLabels = {
  upload: 'Upload Dataset',
  profiling: 'Data Profiling',
  insights: 'Insights',
  ask: 'Ask AI',
  dashboard: 'Dashboard',
}

export default function TopBar() {
  const location = useLocation()
  const { datasetId } = useParams()
  const parts = location.pathname.split('/').filter(Boolean)
  const section = routeLabels[parts[0]] || parts[0]

  return (
    <header className="h-14 border-b border-slate-700/50 bg-ink-900/80 backdrop-blur flex items-center px-6 gap-3 shrink-0">
      <span className="text-slate-500 text-sm font-mono">DataSherlock</span>
      <ChevronRight size={14} className="text-slate-700" />
      <span className="text-sm font-display text-white">{section}</span>
      {datasetId && (
        <>
          <ChevronRight size={14} className="text-slate-700" />
          <span className="text-xs font-mono text-amber-400 bg-amber-400/10 px-2 py-0.5 rounded border border-amber-400/20">
            {datasetId.slice(0, 8)}…
          </span>
        </>
      )}
    </header>
  )
}
