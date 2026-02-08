import { useState, useCallback } from 'react'

interface GenerationResult {
  success: boolean
  content?: string
  model?: string
  task_type?: string
  quality_score?: number
  attempts?: number
  usage?: any
  error?: string
}

interface GenerationProgress {
  stage: string
  progress: number
  message: string
}

export function useGeneration() {
  const [isGenerating, setIsGenerating] = useState(false)
  const [result, setResult] = useState<GenerationResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [progress, setProgress] = useState<GenerationProgress | null>(null)
  const [selectedModel, setSelectedModel] = useState<string>('auto')

  const generate = useCallback(async (
    prompt: string, 
    taskType?: string, 
    model?: string
  ) => {
    setIsGenerating(true)
    setError(null)
    setResult(null)
    setProgress({ stage: 'routing', progress: 10, message: 'Analyzing task type...' })

    try {
      setProgress({ stage: 'generating', progress: 30, message: 'Routing to optimal AI model...' })

      const response = await fetch('/api/generate/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt,
          task_type: taskType,
          preferred_model: model || selectedModel,
        }),
      })

      setProgress({ stage: 'processing', progress: 70, message: 'Generating response...' })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      
      setProgress({ stage: 'complete', progress: 100, message: 'Generation complete!' })
      
      setResult(data)
      
      // Clear progress after a delay
      setTimeout(() => setProgress(null), 2000)
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred'
      setError(errorMessage)
      setProgress(null)
    } finally {
      setIsGenerating(false)
    }
  }, [selectedModel])

  const reset = useCallback(() => {
    setIsGenerating(false)
    setResult(null)
    setError(null)
    setProgress(null)
  }, [])

  return {
    generate,
    isGenerating,
    result,
    error,
    progress,
    selectedModel,
    setSelectedModel,
    reset,
  }
}
