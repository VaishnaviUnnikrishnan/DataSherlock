import { useState, useRef, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { Send, Bot, User, Sparkles } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { askQuestion } from '../services/api'
import Spinner from '../components/ui/Spinner'

const SUGGESTIONS = [
  'Which columns have the most missing data?',
  'What are the key outliers in this dataset?',
  'Summarize the data quality issues.',
  'What machine learning models would suit this data?',
  'Are there any strong correlations I should know about?',
]

function Message({ msg }) {
  const isUser = msg.role === 'user'
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex gap-3 ${isUser ? 'flex-row-reverse' : ''}`}
    >
      <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${isUser ? 'bg-amber-400/10 border border-amber-400/20' : 'bg-slate-800 border border-slate-700'}`}>
        {isUser ? <User size={14} className="text-amber-400" /> : <Bot size={14} className="text-slate-400" />}
      </div>
      <div className={`max-w-[75%] px-4 py-3 rounded-xl text-sm leading-relaxed ${
        isUser
          ? 'bg-amber-400/10 border border-amber-400/20 text-slate-200'
          : 'bg-ink-800 border border-slate-700/50 text-slate-300'
      }`}>
        {msg.content}
      </div>
    </motion.div>
  )
}

export default function AskPage() {
  const { datasetId } = useParams()
  const [messages, setMessages] = useState([
    { role: 'assistant', content: "Hi! I'm DataSherlock. Ask me anything about your dataset — quality issues, patterns, ML recommendations, or specific column stats." }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const send = async (text) => {
    const question = text || input.trim()
    if (!question || loading) return
    setInput('')
    setMessages(m => [...m, { role: 'user', content: question }])
    setLoading(true)
    try {
      const { data } = await askQuestion(datasetId, question)
      setMessages(m => [...m, { role: 'assistant', content: data.answer }])
    } catch (e) {
      setMessages(m => [...m, { role: 'assistant', content: `Error: ${e.message}` }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)]">
      <div className="mb-4">
        <h1 className="font-display text-2xl font-700 text-white">Ask AI</h1>
        <p className="text-slate-500 text-sm font-mono mt-1">Powered by Groq · Llama 3.1 70B</p>
      </div>

      {/* Chat area */}
      <div className="flex-1 overflow-y-auto space-y-4 pr-1">
        {messages.map((msg, i) => <Message key={i} msg={msg} />)}
        {loading && (
          <div className="flex gap-3">
            <div className="w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center">
              <Bot size={14} className="text-slate-400" />
            </div>
            <div className="bg-ink-800 border border-slate-700/50 px-4 py-3 rounded-xl flex items-center gap-2">
              <Spinner size={14} />
              <span className="text-xs font-mono text-slate-500">Thinking…</span>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Suggestions */}
      {messages.length <= 1 && (
        <div className="py-4">
          <p className="label mb-3">Suggested questions</p>
          <div className="flex flex-wrap gap-2">
            {SUGGESTIONS.map(s => (
              <button key={s} onClick={() => send(s)}
                className="text-xs px-3 py-1.5 rounded-lg border border-slate-700 text-slate-400 hover:border-amber-400/30 hover:text-amber-400 transition-all font-body">
                <Sparkles size={10} className="inline mr-1.5 opacity-60" />{s}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input */}
      <div className="pt-3 border-t border-slate-700/50">
        <div className="flex gap-3">
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && !e.shiftKey && send()}
            placeholder="Ask about your data…"
            className="flex-1 bg-ink-900 border border-slate-700 rounded-xl px-4 py-3 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-amber-400/40 transition-colors font-body"
          />
          <button
            onClick={() => send()}
            disabled={!input.trim() || loading}
            className="btn-primary px-4 disabled:opacity-40 disabled:cursor-not-allowed"
          >
            <Send size={16} />
          </button>
        </div>
      </div>
    </div>
  )
}
