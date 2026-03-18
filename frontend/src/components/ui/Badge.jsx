const variants = {
  none: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
  low: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
  medium: 'bg-amber-400/10 text-amber-400 border-amber-400/20',
  high: 'bg-orange-500/10 text-orange-400 border-orange-500/20',
  critical: 'bg-red-500/10 text-red-400 border-red-500/20',
  warning: 'bg-amber-400/10 text-amber-400 border-amber-400/20',
  info: 'bg-cyan-400/10 text-cyan-400 border-cyan-400/20',
  success: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
}

export default function Badge({ label, variant = 'info' }) {
  return (
    <span className={`tag border ${variants[variant] || variants.info}`}>
      {label}
    </span>
  )
}
