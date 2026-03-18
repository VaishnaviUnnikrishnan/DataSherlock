export default function StatCard({ label, value, sub, accent = false, icon: Icon }) {
  return (
    <div className={`card p-5 ${accent ? 'border-amber-400/30 bg-amber-400/5' : ''}`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="label mb-2">{label}</p>
          <p className={`font-display text-2xl font-700 ${accent ? 'text-amber-400' : 'text-white'}`}>
            {value}
          </p>
          {sub && <p className="text-xs text-slate-500 mt-1 font-mono">{sub}</p>}
        </div>
        {Icon && (
          <div className={`p-2 rounded-lg ${accent ? 'bg-amber-400/10 text-amber-400' : 'bg-slate-800 text-slate-400'}`}>
            <Icon size={16} />
          </div>
        )}
      </div>
    </div>
  )
}
