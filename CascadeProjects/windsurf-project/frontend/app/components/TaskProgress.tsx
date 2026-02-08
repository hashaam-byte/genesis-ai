'use client'

import { Card, CardContent } from './ui/card'
import { Badge } from './ui/badge'
import { Loader2, CheckCircle, AlertCircle } from 'lucide-react'

interface TaskProgressProps {
  progress: {
    stage: string
    progress: number
    message: string
  }
}

export default function TaskProgress({ progress }: TaskProgressProps) {
  const getStageIcon = () => {
    switch (progress.stage) {
      case 'complete':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'error':
        return <AlertCircle className="h-4 w-4 text-red-500" />
      default:
        return <Loader2 className="h-4 w-4 animate-spin text-blue-500" />
    }
  }

  const getStageColor = () => {
    switch (progress.stage) {
      case 'complete':
        return 'bg-green-500'
      case 'error':
        return 'bg-red-500'
      default:
        return 'bg-blue-500'
    }
  }

  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex items-center space-x-3">
          {getStageIcon()}
          <div className="flex-1">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium capitalize">{progress.stage}</span>
              <Badge variant="outline">{progress.progress}%</Badge>
            </div>
            <div className="w-full bg-secondary rounded-full h-2">
              <div
                className={`h-2 rounded-full transition-all duration-300 ${getStageColor()}`}
                style={{ width: `${progress.progress}%` }}
              />
            </div>
            <p className="text-sm text-muted-foreground mt-2">{progress.message}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
