import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
      <Toaster
        position="bottom-right"
        toastOptions={{
          style: {
            background: '#0a0f1e',
            color: '#cbd5e1',
            border: '1px solid rgba(251,191,36,0.2)',
            fontFamily: '"DM Sans", sans-serif',
            fontSize: '13px',
          },
          success: {
            iconTheme: { primary: '#fbbf24', secondary: '#050810' },
          },
          error: {
            iconTheme: { primary: '#f87171', secondary: '#050810' },
          },
        }}
      />
    </BrowserRouter>
  </React.StrictMode>
)
