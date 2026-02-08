import { useState, useCallback, useEffect } from 'react'

interface Project {
  id: string
  name: string
  description?: string
  framework?: string
  status: string
  created_at: string
  updated_at: string
  file_count: number
  last_activity?: string
}

interface ProjectFile {
  path: string
  name: string
  size: number
  type: string
  content?: string
  created_at: string
  updated_at: string
}

export function useProjects() {
  const [projects, setProjects] = useState<Project[]>([])
  const [currentProject, setCurrentProject] = useState<Project | null>(null)
  const [files, setFiles] = useState<ProjectFile[]>([])
  const [selectedFile, setSelectedFile] = useState<ProjectFile | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchProjects = useCallback(async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch('/api/projects/')
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setProjects(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch projects')
    } finally {
      setLoading(false)
    }
  }, [])

  const createProject = useCallback(async (name: string, description?: string) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch('/api/projects/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name,
          description,
        }),
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const newProject = await response.json()
      setProjects(prev => [...prev, newProject])
      setCurrentProject(newProject)
      
      return newProject
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create project')
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  const fetchProjectFiles = useCallback(async (projectId: string) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch(`/api/projects/${projectId}/files`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setFiles(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch files')
    } finally {
      setLoading(false)
    }
  }, [])

  const selectFile = useCallback(async (file: ProjectFile | null) => {
    setSelectedFile(file)
    
    if (file && !file.content && currentProject) {
      try {
        const response = await fetch(`/api/projects/${currentProject.id}/files/${file.path}`)
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        const fileData = await response.json()
        setSelectedFile(prev => prev ? { ...prev, content: fileData.content } : null)
      } catch (err) {
        console.error('Failed to fetch file content:', err)
      }
    }
  }, [currentProject])

  const selectProject = useCallback(async (project: Project) => {
    setCurrentProject(project)
    setSelectedFile(null)
    await fetchProjectFiles(project.id)
  }, [fetchProjectFiles])

  const deleteProject = useCallback(async (projectId: string) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch(`/api/projects/${projectId}`, {
        method: 'DELETE',
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      setProjects(prev => prev.filter(p => p.id !== projectId))
      
      if (currentProject?.id === projectId) {
        setCurrentProject(null)
        setFiles([])
        setSelectedFile(null)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete project')
      throw err
    } finally {
      setLoading(false)
    }
  }, [currentProject])

  useEffect(() => {
    fetchProjects()
  }, [fetchProjects])

  return {
    projects,
    currentProject,
    files,
    selectedFile,
    loading,
    error,
    fetchProjects,
    createProject,
    fetchProjectFiles,
    selectFile,
    selectProject,
    deleteProject,
    setSelectedFile,
  }
}
