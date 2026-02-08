'use client'

import { useState } from 'react'
import { Button } from './ui/button'
import { Badge } from './ui/badge'
import { File, Folder, FileText, Code, Image, Video, Music, Archive } from 'lucide-react'

interface ProjectFile {
  path: string
  name: string
  size: number
  type: string
  content?: string
  created_at: string
  updated_at: string
}

interface FileExplorerProps {
  files: ProjectFile[]
  onFileSelect: (file: ProjectFile) => void
}

export default function FileExplorer({ files, onFileSelect }: FileExplorerProps) {
  const [expandedFolders, setExpandedFolders] = useState<Set<string>>(new Set())

  const getFileIcon = (fileName: string, fileType: string) => {
    const extension = fileName.split('.').pop()?.toLowerCase()
    
    if (extension === 'js' || extension === 'jsx' || extension === 'ts' || extension === 'tsx') {
      return <Code className="h-4 w-4 text-blue-500" />
    } else if (extension === 'json' || extension === 'xml' || extension === 'yaml') {
      return <FileText className="h-4 w-4 text-orange-500" />
    } else if (extension === 'png' || extension === 'jpg' || extension === 'jpeg' || extension === 'gif' || extension === 'svg') {
      return <Image className="h-4 w-4 text-green-500" />
    } else if (extension === 'mp4' || extension === 'avi' || extension === 'mov') {
      return <Video className="h-4 w-4 text-purple-500" />
    } else if (extension === 'mp3' || extension === 'wav' || extension === 'ogg') {
      return <Music className="h-4 w-4 text-pink-500" />
    } else if (extension === 'zip' || extension === 'rar' || extension === '7z') {
      return <Archive className="h-4 w-4 text-gray-500" />
    } else {
      return <File className="h-4 w-4 text-gray-400" />
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString()
  }

  const toggleFolder = (path: string) => {
    const newExpanded = new Set(expandedFolders)
    if (newExpanded.has(path)) {
      newExpanded.delete(path)
    } else {
      newExpanded.add(path)
    }
    setExpandedFolders(newExpanded)
  }

  const organizeFiles = (files: ProjectFile[]) => {
    const tree: Record<string, ProjectFile[]> = {}
    
    files.forEach(file => {
      const parts = file.path.split('/')
      if (parts.length > 1) {
        const folder = parts[0]
        if (!tree[folder]) {
          tree[folder] = []
        }
        tree[folder].push(file)
      } else {
        if (!tree['root']) {
          tree['root'] = []
        }
        tree['root'].push(file)
      }
    })
    
    return tree
  }

  const fileTree = organizeFiles(files)

  if (files.length === 0) {
    return (
      <div className="text-center py-8">
        <File className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
        <p className="text-muted-foreground">No files in this project yet</p>
        <p className="text-sm text-muted-foreground mt-2">
          Generate some code to see files appear here
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between p-2 border-b">
        <h3 className="font-medium text-sm">Project Files</h3>
        <Badge variant="outline">{files.length} files</Badge>
      </div>
      
      <div className="max-h-96 overflow-y-auto">
        {Object.entries(fileTree).map(([folderName, folderFiles]) => (
          <div key={folderName} className="mb-4">
            {folderName !== 'root' && (
              <div 
                className="flex items-center space-x-2 p-2 hover:bg-muted cursor-pointer rounded"
                onClick={() => toggleFolder(folderName)}
              >
                <Folder className="h-4 w-4 text-yellow-500" />
                <span className="text-sm font-medium">{folderName}</span>
                <Badge variant="outline" className="text-xs">
                  {folderFiles.length}
                </Badge>
              </div>
            )}
            
            {(folderName === 'root' || expandedFolders.has(folderName)) && (
              <div className={folderName !== 'root' ? 'ml-4' : ''}>
                {folderFiles.map((file) => (
                  <div
                    key={file.path}
                    className="flex items-center space-x-3 p-2 hover:bg-muted cursor-pointer rounded group"
                    onClick={() => onFileSelect(file)}
                  >
                    {getFileIcon(file.name, file.type)}
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium truncate">{file.name}</p>
                      <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                        <span>{formatFileSize(file.size)}</span>
                        <span>•</span>
                        <span>{formatDate(file.updated_at)}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
