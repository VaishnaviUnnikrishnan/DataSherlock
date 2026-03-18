import { useState, useCallback } from 'react'

export function useDataset() {
  const [dataset, setDataset] = useState(() => {
    const stored = sessionStorage.getItem('ds_dataset')
    return stored ? JSON.parse(stored) : null
  })

  const saveDataset = useCallback((data) => {
    setDataset(data)
    sessionStorage.setItem('ds_dataset', JSON.stringify(data))
  }, [])

  const clearDataset = useCallback(() => {
    setDataset(null)
    sessionStorage.removeItem('ds_dataset')
  }, [])

  return { dataset, saveDataset, clearDataset }
}
