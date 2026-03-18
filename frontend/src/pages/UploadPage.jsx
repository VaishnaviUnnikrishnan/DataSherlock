import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { useNavigate } from 'react-router-dom'
import { Upload, FileText, CheckCircle, AlertCircle, X } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import toast from 'react-hot-toast'
import { uploadFile } from '../services/api'
import Spinner from '../components/ui/Spinner'

const ACCEPTED = { 'text/csv': ['.csv'], 'application/json': ['.json'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'], 'application/octet-stream': ['.parquet'] }

export default function UploadPage() {
  const [file, setFile] = useState(null)
  const [progress, setProgress] = useState(0)
  const [status, setStatus] = useState('idle') // idle | uploading | success | error
  const [result, setResult] = useState(null)
  const navigate = useNavigate()

  const onDrop = useCallback((accepted) => {
    if (accepted[0]) { setFile(accepted[0]); setStatus('idle') }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop, accept: ACCEPTED, maxFiles: 1, maxSize: 100 * 1024 * 1024,
  })

  const handleUpload = async () => {
    if (!file) return
    setStatus('uploading')
    setProgress(0)
    try {
      const { data } = await uploadFile(file, setProgress)
      setResult(data)
      setStatus('success')
      toast.success(`Dataset uploaded — ${data.rows.toLocaleString()} rows`)
    } catch (e) {
      setStatus('error')
      toast.error(e.message)
    }
  }

  const handleContinue = () => result && navigate(`/profiling/${result.dataset_id}`)

  return (
    <div className="max-w-2xl mx-auto py-8">
      <div className="mb-8">
        <h1 className="font-display text-3xl font-700 text-white mb-2">Upload Dataset</h1>
        <p className="text-slate-400 text-sm">Supports CSV, Excel, JSON, and Parquet files up to 100MB.</p>
      </div>

      {/* Dropzone */}
      <div
        {...getRootProps()}
        className={`relative border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-all duration-300 ${
          isDragActive
            ? 'border-amber-400 bg-amber-400/5'
            : file
            ? 'border-slate-600 bg-slate-800/30'
            : 'border-slate-700 hover:border-slate-500 hover:bg-slate-800/20'
        }`}
      >
        <input {...getInputProps()} />
        <AnimatePresence mode="wait">
          {file ? (
            <motion.div key="file" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="flex flex-col items-center gap-3">
              <div className="w-12 h-12 rounded-xl bg-amber-400/10 border border-amber-400/20 flex items-center justify-center">
                <FileText size={22} className="text-amber-400" />
              </div>
              <div>
                <p className="font-display text-white font-600">{file.name}</p>
                <p className="text-sm text-slate-500 font-mono">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
              </div>
              <button onClick={(e) => { e.stopPropagation(); setFile(null); setStatus('idle') }}
                className="flex items-center gap-1 text-xs text-slate-500 hover:text-red-400 transition-colors mt-1">
                <X size={12} /> Remove
              </button>
            </motion.div>
          ) : (
            <motion.div key="empty" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex flex-col items-center gap-4">
              <div className="w-14 h-14 rounded-2xl bg-slate-800 flex items-center justify-center">
                <Upload size={24} className="text-slate-400" />
              </div>
              <div>
                <p className="font-display text-white text-lg font-600 mb-1">
                  {isDragActive ? 'Drop it here' : 'Drag & drop your dataset'}
                </p>
                <p className="text-sm text-slate-500">or click to browse files</p>
              </div>
              <div className="flex gap-2">
                {['.csv', '.xlsx', '.json', '.parquet'].map(ext => (
                  <span key={ext} className="tag bg-slate-800 text-slate-400 border border-slate-700">{ext}</span>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Progress */}
      {status === 'uploading' && (
        <div className="mt-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-mono text-slate-500">Uploading & processing…</span>
            <span className="text-xs font-mono text-amber-400">{progress}%</span>
          </div>
          <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-amber-400 rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.3 }}
            />
          </div>
        </div>
      )}

      {/* Success result */}
      <AnimatePresence>
        {status === 'success' && result && (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-4 card-glow p-5">
            <div className="flex items-start gap-3">
              <CheckCircle size={18} className="text-emerald-400 mt-0.5 shrink-0" />
              <div className="flex-1">
                <p className="font-display text-white font-600 mb-3">Upload successful</p>
                <div className="grid grid-cols-3 gap-3">
                  {[
                    { label: 'Rows', value: result.rows?.toLocaleString() },
                    { label: 'Columns', value: result.columns },
                    { label: 'Dataset ID', value: result.dataset_id?.slice(0, 8) + '…' },
                  ].map(({ label, value }) => (
                    <div key={label} className="bg-ink-950/50 rounded-lg p-3">
                      <p className="label mb-1">{label}</p>
                      <p className="font-mono text-white text-sm">{value}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Actions */}
      <div className="mt-6 flex gap-3">
        {status !== 'success' ? (
          <button
            onClick={handleUpload}
            disabled={!file || status === 'uploading'}
            className="btn-primary flex items-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed"
          >
            {status === 'uploading' ? <><Spinner size={15} /> Processing…</> : <><Upload size={15} /> Upload & Analyse</>}
          </button>
        ) : (
          <button onClick={handleContinue} className="btn-primary flex items-center gap-2">
            View Profiling Report →
          </button>
        )}
        {file && status !== 'uploading' && (
          <button onClick={() => { setFile(null); setStatus('idle'); setResult(null) }} className="btn-ghost">
            Clear
          </button>
        )}
      </div>
    </div>
  )
}
