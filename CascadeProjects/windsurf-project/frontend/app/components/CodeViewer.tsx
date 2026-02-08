'use client'

import { useState } from 'react'
import { Button } from './ui/button'
import { Badge } from './ui/badge'
import { Copy, Download, Eye, Code } from 'lucide-react'

interface CodeViewerProps {
  content: string
  language?: string
  title?: string
}

export default function CodeViewer({ content, language = 'text', title }: CodeViewerProps) {
  const [copied, setCopied] = useState(false)

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(content)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  const downloadFile = () => {
    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = title || `code.${language === 'typescript' ? 'ts' : language === 'javascript' ? 'js' : 'txt'}`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const getLanguageColor = (lang: string) => {
    const colors: Record<string, string> = {
      javascript: 'bg-yellow-500',
      typescript: 'bg-blue-500',
      python: 'bg-green-500',
      html: 'bg-orange-500',
      css: 'bg-purple-500',
      json: 'bg-gray-500',
      text: 'bg-gray-400',
    }
    return colors[lang] || colors.text
  }

  return (
    <div className="border border-border rounded-lg overflow-hidden">
      {/* Header */}
      <div className="bg-muted border-b border-border px-4 py-2 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Code className="h-4 w-4" />
          <span className="text-sm font-medium">{title || 'Generated Code'}</span>
          <Badge 
            variant="outline" 
            className={`text-xs ${getLanguageColor(language)} text-white border-0`}
          >
            {language}
          </Badge>
        </div>
        
        <div className="flex items-center space-x-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={copyToClipboard}
            className="h-8 w-8 p-0"
          >
            {copied ? (
              <Eye className="h-4 w-4 text-green-500" />
            ) : (
              <Copy className="h-4 w-4" />
            )}
          </Button>
          
          <Button
            variant="ghost"
            size="sm"
            onClick={downloadFile}
            className="h-8 w-8 p-0"
          >
            <Download className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Code Content */}
      <div className="relative">
        <pre className="p-4 overflow-x-auto text-sm bg-background">
          <code className={`language-${language}`}>
            {content}
          </code>
        </pre>
        
        {/* Line numbers overlay (simplified) */}
        <div className="absolute left-0 top-0 bottom-0 w-12 bg-muted/50 border-r border-border pointer-events-none">
          <div className="text-xs text-muted-foreground text-right pr-2 pt-4">
            {content.split('\n').map((_, index) => (
              <div key={index}>{index + 1}</div>
            ))}
          </div>
        </div>
      </div>

      {/* Footer with stats */}
      <div className="bg-muted/50 border-t border-border px-4 py-2">
        <div className="flex items-center justify-between text-xs text-muted-foreground">
          <span>{content.split('\n').length} lines</span>
          <span>{content.length} characters</span>
        </div>
      </div>
    </div>
  )
}
