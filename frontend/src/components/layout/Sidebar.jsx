import { NavLink, useParams } from 'react-router-dom'
import { Upload, BarChart2, Lightbulb, MessageSquare, LayoutDashboard, Zap } from 'lucide-react'
import clsx from 'clsx'

const Logo = () => (
  <div className="flex items-center gap-3 px-5 py-6 border-b border-slate-700/50">
    <div className="relative w-8 h-8">
      <div className="absolute inset-0 bg-amber-400 rounded-lg rotate-12 opacity-20" />
      <div className="absolute inset-0 flex items-center justify-center">
        <Zap size={18} className="text-amber-400" />
      </div>
    </div>
    <div>
      <p className="font-display font-700 text-white text-base leading-none">DataSherlock</p>
      <p className="text-[10px] font-mono text-slate-500 mt-0.5 tracking-widest uppercase">Intelligence Layer</p>
    </div>
  </div>
)

export default function Sidebar() {
  const { datasetId } = useParams()
  const id = datasetId || ''

  const navItems = [
    { to: '/upload', icon: Upload, label: 'Upload', always: true },
    { to: `/profiling/${id}`, icon: BarChart2, label: 'Profiling', disabled: !id },
    { to: `/insights/${id}`, icon: Lightbulb, label: 'Insights', disabled: !id },
    { to: `/ask/${id}`, icon: MessageSquare, label: 'Ask AI', disabled: !id },
    { to: `/dashboard/${id}`, icon: LayoutDashboard, label: 'Dashboard', disabled: !id },
  ]

  return (
    <aside className="w-56 bg-ink-900 border-r border-slate-700/50 flex flex-col shrink-0">
      <Logo />
      <nav className="flex-1 px-3 py-4 space-y-0.5">
        {navItems.map(({ to, icon: Icon, label, disabled, always }) => (
          disabled ? (
            <div key={label} className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-600 cursor-not-allowed">
              <Icon size={15} />
              <span className="text-sm font-body">{label}</span>
            </div>
          ) : (
            <NavLink
              key={label}
              to={to}
              className={({ isActive }) => clsx(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-150 text-sm',
                isActive
                  ? 'bg-amber-400/10 text-amber-400 border border-amber-400/20'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              )}
            >
              <Icon size={15} />
              <span className="font-body">{label}</span>
            </NavLink>
          )
        ))}
      </nav>
      <div className="px-4 py-4 border-t border-slate-700/50">
        <div className="flex items-center gap-2">
          <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
          <span className="text-xs font-mono text-slate-500">API connected</span>
        </div>
      </div>
    </aside>
  )
}
