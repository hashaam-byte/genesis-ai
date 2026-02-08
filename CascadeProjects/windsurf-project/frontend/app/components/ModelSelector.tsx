'use client'

import { useState } from 'react'
import { Button } from './ui/button'
import { Badge } from './ui/badge'
import { Brain, Cpu, Zap, Globe } from 'lucide-react'

interface ModelSelectorProps {
  selectedModel: string
  onModelChange: (model: string) => void
}

const models = [
  { id: 'auto', name: 'Auto-detect', icon: Brain, description: 'Smart routing to best model' },
  { id: 'claude', name: 'Claude', icon: Brain, description: 'Creative tasks, complex reasoning' },
  { id: 'gpt-4', name: 'GPT-4', icon: Cpu, description: 'General coding, tool use' },
  { id: 'gemini', name: 'Gemini', icon: Globe, description: 'Multimodal tasks' },
  { id: 'groq', name: 'Groq', icon: Zap, description: 'Fast inference' },
]

export default function ModelSelector({ selectedModel, onModelChange }: ModelSelectorProps) {
  const [isOpen, setIsOpen] = useState(false)

  const selectedModelData = models.find(m => m.id === selectedModel) || models[0]
  const Icon = selectedModelData.icon

  return (
    <div className="relative">
      <Button
        variant="outline"
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2"
      >
        <Icon className="h-4 w-4" />
        <span>{selectedModelData.name}</span>
      </Button>

      {isOpen && (
        <div className="absolute top-full mt-2 w-64 bg-background border border-border rounded-lg shadow-lg z-50">
          <div className="p-2">
            {models.map((model) => {
              const ModelIcon = model.icon
              return (
                <button
                  key={model.id}
                  onClick={() => {
                    onModelChange(model.id)
                    setIsOpen(false)
                  }}
                  className={`w-full text-left p-3 rounded-lg hover:bg-muted transition-colors ${
                    selectedModel === model.id ? 'bg-muted border border-primary' : ''
                  }`}
                >
                  <div className="flex items-start space-x-3">
                    <ModelIcon className="h-4 w-4 mt-0.5 text-primary" />
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <h4 className="font-medium text-sm">{model.name}</h4>
                        {selectedModel === model.id && (
                          <Badge variant="default" className="text-xs">Active</Badge>
                        )}
                      </div>
                      <p className="text-xs text-muted-foreground mt-1">
                        {model.description}
                      </p>
                    </div>
                  </div>
                </button>
              )
            })}
          </div>
        </div>
      )}

      {/* Click outside to close */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => setIsOpen(false)}
        />
      )}
    </div>
  )
}
