'use client'

import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { AlertTriangle, RefreshCw } from 'lucide-react'

interface ErrorDisplayProps {
  error: string
  onRetry?: () => void
}

export default function ErrorDisplay({ error, onRetry }: ErrorDisplayProps) {
  return (
    <Card className="border-destructive/50 bg-destructive/5">
      <CardHeader>
        <CardTitle className="flex items-center space-x-2 text-destructive">
          <AlertTriangle className="h-5 w-5" />
          <span>Generation Error</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <p className="text-sm text-muted-foreground">{error}</p>
          
          {onRetry && (
            <Button 
              onClick={onRetry}
              variant="outline"
              size="sm"
              className="mt-2"
            >
              <RefreshCw className="h-4 w-4 mr-2" />
              Try Again
            </Button>
          )}
          
          <div className="text-xs text-muted-foreground bg-muted p-3 rounded-md">
            <strong>Troubleshooting tips:</strong>
            <ul className="mt-1 space-y-1">
              <li>• Check your API key configuration</li>
              <li>• Ensure you have credits available</li>
              <li>• Try a simpler prompt</li>
              <li>• Check network connectivity</li>
            </ul>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
