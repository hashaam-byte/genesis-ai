'use client'

import { useState } from 'react'
import { Button } from './ui/button'
import { Textarea } from './ui/textarea'
import { Badge } from './ui/badge'
import { Sparkles, Send, Loader2 } from 'lucide-react'

interface TaskType {
  id: string
  name: string
  icon: any
  description: string
}

interface PromptInputProps {
  onGenerate: (prompt: string, taskType?: string) => void
  isGenerating: boolean
  taskTypes: TaskType[]
}

export default function PromptInput({ onGenerate, isGenerating, taskTypes }: PromptInputProps) {
  const [prompt, setPrompt] = useState('')
  const [selectedTaskType, setSelectedTaskType] = useState<string>('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (prompt.trim() && !isGenerating) {
      onGenerate(prompt.trim(), selectedTaskType || undefined)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
      handleSubmit(e as any)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Task Type Selection */}
      <div className="space-y-2">
        <label className="text-sm font-medium">Task Type (Optional)</label>
        <div className="flex flex-wrap gap-2">
          <Badge
            variant={selectedTaskType === '' ? 'default' : 'outline'}
            className="cursor-pointer"
            onClick={() => setSelectedTaskType('')}
          >
            Auto-detect
          </Badge>
          {taskTypes.map((type) => {
            const Icon = type.icon
            return (
              <Badge
                key={type.id}
                variant={selectedTaskType === type.id ? 'default' : 'outline'}
                className="cursor-pointer flex items-center gap-1"
                onClick={() => setSelectedTaskType(type.id)}
              >
                <Icon className="h-3 w-3" />
                {type.name}
              </Badge>
            )
          })}
        </div>
      </div>

      {/* Prompt Input */}
      <div className="space-y-2">
        <label className="text-sm font-medium">Describe what you want to create</label>
        <Textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Create a modern e-commerce website with React and TypeScript..."
          className="min-h-[120px] resize-none border-2 focus:border-primary"
          disabled={isGenerating}
        />
        <p className="text-xs text-muted-foreground">
          Press Cmd/Ctrl + Enter to generate
        </p>
      </div>

      {/* Submit Button */}
      <div className="flex items-center justify-between">
        <div className="text-sm text-muted-foreground">
          {prompt.length > 0 && (
            <span>{prompt.length} characters</span>
          )}
        </div>
        
        <Button 
          type="submit" 
          disabled={!prompt.trim() || isGenerating}
          className="min-w-[120px]"
        >
          {isGenerating ? (
            <>
              <Loader2 className="h-4 w-4 mr-2 animate-spin" />
              Generating...
            </>
          ) : (
            <>
              <Sparkles className="h-4 w-4 mr-2" />
              Generate
            </>
          )}
        </Button>
      </div>
    </form>
  )
}
