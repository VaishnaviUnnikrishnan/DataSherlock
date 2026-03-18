import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 60000,
})

api.interceptors.response.use(
  res => res,
  err => {
    const msg = err.response?.data?.detail || err.message || 'Something went wrong'
    return Promise.reject(new Error(msg))
  }
)

export const uploadFile = (file, onProgress) => {
  const form = new FormData()
  form.append('file', file)
  return api.post('/upload/', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: e => onProgress && onProgress(Math.round((e.loaded * 100) / e.total)),
  })
}

export const getDatasetInfo = (id) => api.get(`/upload/${id}`)
export const getProfile = (id) => api.get(`/profiling/${id}`)
export const getDrift = (id, refId) => api.get(`/profiling/${id}/drift?reference_id=${refId}`)
export const getInsights = (id) => api.get(`/insights/${id}`)
export const askQuestion = (datasetId, question) => api.post('/ask/', { dataset_id: datasetId, question })
export const generateDashboard = (id) => api.post(`/dashboard/${id}/generate`)

export default api
