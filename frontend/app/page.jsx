'use client'
import React, { useState } from 'react';
import { Send, Loader2, CheckCircle, XCircle, Code2, Folder } from 'lucide-react';

export default function GenesisAI() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const generateProject = async () => {
    if (!prompt.trim()) return;

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
      });

      if (!response.ok) throw new Error('Generation failed');

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'Failed to connect to backend');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <div className="border-b border-purple-500/20 bg-black/40 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center gap-3">
            <Code2 className="w-8 h-8 text-purple-400" />
            <div>
              <h1 className="text-2xl font-bold text-white">GENESIS AI</h1>
              <p className="text-xs text-purple-300">Ultimate Autonomous Builder</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Prompt Input */}
        <div className="bg-black/40 backdrop-blur-sm border border-purple-500/30 rounded-xl p-6 mb-6">
          <label className="block text-purple-200 font-medium mb-3">
            What do you want to build?
          </label>
          <div className="flex gap-3">
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Example: Build a todo web app with React and Node.js backend..."
              className="flex-1 bg-slate-900/50 border border-purple-500/30 rounded-lg px-4 py-3 text-white placeholder-purple-300/50 focus:outline-none focus:border-purple-400 resize-none"
              rows={3}
              disabled={loading}
            />
            <button
              onClick={generateProject}
              disabled={loading || !prompt.trim()}
              className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 disabled:from-gray-600 disabled:to-gray-600 text-white font-medium rounded-lg flex items-center gap-2 transition-all disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Building...
                </>
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  Generate
                </>
              )}
            </button>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4 mb-6">
            <div className="flex items-center gap-2 text-red-400">
              <XCircle className="w-5 h-5" />
              <span className="font-medium">Error: {error}</span>
            </div>
            <p className="text-sm text-red-300/70 mt-2">
              Make sure Python backend is running on port 8000
            </p>
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="space-y-6">
            {/* Status */}
            <div className="bg-black/40 backdrop-blur-sm border border-purple-500/30 rounded-xl p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-white">Project Status</h2>
                <div className="flex items-center gap-2">
                  {result.status === 'complete' ? (
                    <>
                      <CheckCircle className="w-5 h-5 text-green-400" />
                      <span className="text-green-400 font-medium">Complete</span>
                    </>
                  ) : (
                    <>
                      <XCircle className="w-5 h-5 text-red-400" />
                      <span className="text-red-400 font-medium">Failed</span>
                    </>
                  )}
                </div>
              </div>
              <div className="text-sm text-purple-300">
                Project ID: <span className="font-mono">{result.project_id}</span>
              </div>
            </div>

            {/* Execution Plan */}
            <div className="bg-black/40 backdrop-blur-sm border border-purple-500/30 rounded-xl p-6">
              <h3 className="text-lg font-bold text-white mb-4">Execution Plan</h3>
              <div className="space-y-3">
                {result.plan.map((step) => (
                  <div
                    key={step.step_number}
                    className="flex items-start gap-3 bg-slate-900/50 rounded-lg p-3 border border-purple-500/20"
                  >
                    <div className="flex-shrink-0">
                      {step.status === 'complete' ? (
                        <CheckCircle className="w-5 h-5 text-green-400" />
                      ) : step.status === 'running' ? (
                        <Loader2 className="w-5 h-5 text-blue-400 animate-spin" />
                      ) : step.status === 'failed' ? (
                        <XCircle className="w-5 h-5 text-red-400" />
                      ) : (
                        <div className="w-5 h-5 rounded-full border-2 border-purple-500/30" />
                      )}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <span className="text-purple-300 font-medium">
                          Step {step.step_number}
                        </span>
                        <span className="text-white">{step.description}</span>
                      </div>
                      {step.output && (
                        <p className="text-sm text-green-400 mt-1">{step.output}</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Files Created */}
            {result.files_created.length > 0 && (
              <div className="bg-black/40 backdrop-blur-sm border border-purple-500/30 rounded-xl p-6">
                <div className="flex items-center gap-2 mb-4">
                  <Folder className="w-5 h-5 text-purple-400" />
                  <h3 className="text-lg font-bold text-white">Files Created</h3>
                </div>
                <div className="space-y-2">
                  {result.files_created.map((file, idx) => (
                    <div
                      key={idx}
                      className="bg-slate-900/50 rounded px-3 py-2 font-mono text-sm text-purple-300"
                    >
                      {file}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Logs */}
            {result.logs.length > 0 && (
              <div className="bg-black/40 backdrop-blur-sm border border-purple-500/30 rounded-xl p-6">
                <h3 className="text-lg font-bold text-white mb-4">Execution Logs</h3>
                <div className="bg-slate-950 rounded-lg p-4 font-mono text-xs space-y-1 max-h-64 overflow-y-auto">
                  {result.logs.map((log, idx) => (
                    <div key={idx} className="text-green-400">
                      {log}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Errors */}
            {result.errors.length > 0 && (
              <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-6">
                <h3 className="text-lg font-bold text-red-400 mb-4">Errors</h3>
                <div className="space-y-2">
                  {result.errors.map((err, idx) => (
                    <div key={idx} className="text-sm text-red-300">
                      • {err}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Getting Started */}
        {!result && !loading && (
          <div className="bg-black/40 backdrop-blur-sm border border-purple-500/30 rounded-xl p-8 text-center">
            <Code2 className="w-16 h-16 text-purple-400 mx-auto mb-4" />
            <h3 className="text-xl font-bold text-white mb-2">Ready to Build</h3>
            <p className="text-purple-300 mb-6">
              Enter your project idea above and GENESIS AI will create it for you
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-left">
              <div className="bg-slate-900/50 rounded-lg p-4 border border-purple-500/20">
                <div className="text-purple-400 font-medium mb-1">Web Apps</div>
                <div className="text-sm text-purple-300/70">React, Next.js, Node.js</div>
              </div>
              <div className="bg-slate-900/50 rounded-lg p-4 border border-purple-500/20">
                <div className="text-purple-400 font-medium mb-1">Games</div>
                <div className="text-sm text-purple-300/70">Unity, Blender, 3D</div>
              </div>
              <div className="bg-slate-900/50 rounded-lg p-4 border border-purple-500/20">
                <div className="text-purple-400 font-medium mb-1">Mobile Apps</div>
                <div className="text-sm text-purple-300/70">React Native, Flutter</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}