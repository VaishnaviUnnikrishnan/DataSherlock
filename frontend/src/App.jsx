import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/layout/Layout'
import UploadPage from './pages/UploadPage'
import ProfilingPage from './pages/ProfilingPage'
import InsightsPage from './pages/InsightsPage'
import AskPage from './pages/AskPage'
import DashboardPage from './pages/DashboardPage'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Navigate to="/upload" replace />} />
        <Route path="upload" element={<UploadPage />} />
        <Route path="profiling/:datasetId" element={<ProfilingPage />} />
        <Route path="insights/:datasetId" element={<InsightsPage />} />
        <Route path="ask/:datasetId" element={<AskPage />} />
        <Route path="dashboard/:datasetId" element={<DashboardPage />} />
      </Route>
    </Routes>
  )
}
