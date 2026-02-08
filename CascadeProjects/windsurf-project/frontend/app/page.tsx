'use client'

import { useState } from 'react'
import PromptInput from '../app/components/PromptInput'
import TaskProgress from '../app/components/TaskProgress'
import FileExplorer from '../app/components/FileExplorer'
import CodeViewer from '../app/components/CodeViewer'
import ModelSelector from '../app/components/ModelSelector'
import ErrorDisplay from '../app/components/ErrorDisplay'
import { useGeneration } from '../app/hooks/useGeneration'
import { useProjects } from '../app/hooks/useProjects'
import { Button } from '../app/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../app/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../app/components/ui/tabs'
import { Badge } from '../app/components/ui/badge'
import { Sparkles, Code, Zap, Brain, Globe, Gamepad2, Palette, Settings } from 'lucide-react'

export default function Home() {
  const [activeTab, setActiveTab] = useState('generate')
  const { 
    generate, 
    isGenerating, 
    result, 
    error, 
    progress,
    selectedModel,
    setSelectedModel 
  } = useGeneration()
  
  const { 
    projects, 
    currentProject, 
    createProject, 
    files,
    selectedFile,
    selectFile 
  } = useProjects()

  const handleGenerate = async (prompt: string, taskType?: string) => {
    await generate(prompt, taskType, selectedModel)
  }

  const taskTypes = [
    { id: 'creative_ui', name: 'Creative UI', icon: Palette, description: 'Design beautiful interfaces' },
    { id: 'code_generation', name: 'Code Generation', icon: Code, description: 'Generate clean, maintainable code' },
    { id: 'architecture', name: 'Architecture', icon: Globe, description: 'Design scalable systems' },
    { id: 'debugging', name: 'Debugging', icon: Settings, description: 'Fix bugs and issues' },
    { id: 'fast_simple', name: 'Quick Tasks', icon: Zap, description: 'Fast, simple generation' },
    { id: '3d_modeling', name: '3D & Games', icon: Gamepad2, description: 'Unity, Blender, games' },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-muted/20">
      {/* Header */}
      <header className="border-b border-border/50 bg-background/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 rounded-lg genesis-gradient">
                <Brain className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-foreground">GENESIS AI</h1>
                <p className="text-sm text-muted-foreground">Hybrid Orchestrator System</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <ModelSelector 
                selectedModel={selectedModel}
                onModelChange={setSelectedModel}
              />
              <Badge variant="outline" className="hidden sm:flex">
                <Sparkles className="h-3 w-3 mr-1" />
                Multi-Model AI
              </Badge>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="generate">Generate</TabsTrigger>
            <TabsTrigger value="projects">Projects</TabsTrigger>
            <TabsTrigger value="explore">Explore</TabsTrigger>
          </TabsList>

          {/* Generate Tab */}
          <TabsContent value="generate" className="space-y-6">
            <div className="grid lg:grid-cols-3 gap-6">
              {/* Main Input Area */}
              <div className="lg:col-span-2 space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <Sparkles className="h-5 w-5" />
                      <span>AI Generation</span>
                    </CardTitle>
                    <CardDescription>
                      Describe what you want to create. GENESIS AI will route to the best model.
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <PromptInput 
                      onGenerate={handleGenerate}
                      isGenerating={isGenerating}
                      taskTypes={taskTypes}
                    />
                  </CardContent>
                </Card>

                {/* Progress Display */}
                {isGenerating && (
                  <TaskProgress progress={progress} />
                )}

                {/* Error Display */}
                {error && (
                  <ErrorDisplay error={error} />
                )}

                {/* Result Display */}
                {result && (
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center justify-between">
                        <span>Generated Result</span>
                        <div className="flex items-center space-x-2">
                          <Badge variant="outline">
                            {result.model}
                          </Badge>
                          {result.quality_score && (
                            <Badge variant="secondary">
                              Quality: {Math.round(result.quality_score * 100)}%
                            </Badge>
                          )}
                        </div>
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <CodeViewer 
                        content={result.content}
                        language="typescript"
                      />
                    </CardContent>
                  </Card>
                )}
              </div>

              {/* Sidebar */}
              <div className="space-y-6">
                {/* Task Type Guide */}
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Task Types</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {taskTypes.map((type) => {
                      const Icon = type.icon
                      return (
                        <div 
                          key={type.id}
                          className="flex items-start space-x-3 p-3 rounded-lg border border-border/50 hover:bg-muted/50 transition-colors cursor-pointer"
                        >
                          <Icon className="h-4 w-4 mt-0.5 text-primary" />
                          <div className="flex-1">
                            <h4 className="font-medium text-sm">{type.name}</h4>
                            <p className="text-xs text-muted-foreground">
                              {type.description}
                            </p>
                          </div>
                        </div>
                      )
                    })}
                  </CardContent>
                </Card>

                {/* Quick Actions */}
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Quick Actions</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <Button 
                      variant="outline" 
                      className="w-full justify-start"
                      onClick={() => createProject('New Project')}
                    >
                      <Code className="h-4 w-4 mr-2" />
                      New Project
                    </Button>
                    <Button 
                      variant="outline" 
                      className="w-full justify-start"
                      onClick={() => setActiveTab('projects')}
                    >
                      <Globe className="h-4 w-4 mr-2" />
                      View Projects
                    </Button>
                  </CardContent>
                </Card>
              </div>
            </div>
          </TabsContent>

          {/* Projects Tab */}
          <TabsContent value="projects" className="space-y-6">
            <div className="grid lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2">
                <Card>
                  <CardHeader>
                    <CardTitle>Project Files</CardTitle>
                    <CardDescription>
                      {currentProject ? `Files in ${currentProject.name}` : 'Select a project to view files'}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    {selectedFile ? (
                      <CodeViewer 
                        content={selectedFile.content}
                        language={selectedFile.name.split('.').pop() || 'text'}
                      />
                    ) : (
                      <FileExplorer 
                        files={files}
                        onFileSelect={selectFile}
                      />
                    )}
                  </CardContent>
                </Card>
              </div>
              
              <div>
                <Card>
                  <CardHeader>
                    <CardTitle>Projects</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      {projects.map((project) => (
                        <div 
                          key={project.id}
                          className={`p-3 rounded-lg border cursor-pointer transition-colors ${
                            currentProject?.id === project.id 
                              ? 'border-primary bg-primary/5' 
                              : 'border-border hover:bg-muted/50'
                          }`}
                          onClick={() => selectFile(null)} // This would select the project
                        >
                          <h4 className="font-medium">{project.name}</h4>
                          <p className="text-sm text-muted-foreground">
                            {project.file_count} files
                          </p>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </TabsContent>

          {/* Explore Tab */}
          <TabsContent value="explore" className="space-y-6">
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Brain className="h-5 w-5" />
                    <span>Smart Routing</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    GENESIS AI automatically routes your requests to the best AI model 
                    based on task type, complexity, and availability.
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Zap className="h-5 w-5" />
                    <span>Multi-Model</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    Leverages Claude, GPT-4, Gemini, and Groq to cover each other's 
                    weaknesses and provide comprehensive solutions.
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Code className="h-5 w-5" />
                    <span>Full-Stack</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    Generate complete applications including frontend, backend, 
                    databases, authentication, and deployment configurations.
                  </p>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}
