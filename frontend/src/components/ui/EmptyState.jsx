export default function EmptyState({ icon: Icon, title, description }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center">
      {Icon && (
        <div className="w-14 h-14 rounded-2xl bg-slate-800 flex items-center justify-center mb-4">
          <Icon size={24} className="text-slate-500" />
        </div>
      )}
      <p className="font-display text-white text-lg mb-2">{title}</p>
      <p className="text-slate-500 text-sm max-w-xs">{description}</p>
    </div>
  )
}
