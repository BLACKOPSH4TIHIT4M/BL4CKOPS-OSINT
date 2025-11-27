"use client"

import { useState } from "react"
import { OSINTTerminal } from "@/components/OSINTTerminal"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card } from "@/components/ui/card"
import { Database, Search, User, Shield, Unlock, Lock } from "lucide-react"

interface TerminalLog {
  timestamp: string
  type: "info" | "success" | "error" | "result"
  message: string
  link?: string
}

interface TerminalLog {
  timestamp: string
  type: "info" | "success" | "error" | "result"
  message: string
  link?: string
}

// Module definitions dengan kekhususan masing-masing
const MODULES = {
  dump: [
    { id: "1", name: "DUMP", description: "DUMP EMAIL PASS", moduleId: "A135" },
    { id: "2", name: "DUMP", description: "DUMP APACHE PASS", moduleId: "A166" },
    { id: "3", name: "DUMP", description: "DUMP SQL USER PASS", moduleId: "A196" },
    { id: "4", name: "DUMP", description: "DUMP APIKEYS", moduleId: "A121" },
    { id: "5", name: "DUMP", description: "DUMP COOKIES", moduleId: "A115" },
  ],
  scrapper: [
    { id: "1", name: "FILES", description: "FILES SCRAPPING", moduleId: "A235" },
    { id: "2", name: "NUMBERS", description: "NUMBERS SCRAPPING", moduleId: "A312" },
    { id: "3", name: "EMAILS", description: "EMAILS SCRAPPING", moduleId: "A221" },
    { id: "4", name: "PAGES", description: "PAGES SCRAPPING", moduleId: "A186" },
    { id: "5", name: "OTHER", description: "OTHER SCRAPPING", moduleId: "A189" },
    { id: "6", name: "PASS", description: "PASS SCRAPPING", moduleId: "A102" },
  ],
  advanced: [
    { id: "7", name: "PERSON", description: "PERSON SEARCHER", moduleId: "A451" },
    { id: "8", name: "FULL", description: "FULL SCRAPPER", moduleId: "A999" },
    { id: "9", name: "CLASS", description: "CLASS MODE", moduleId: "A777" },
  ]
}

const MODULE_TO_OSINT = {
  "A135": "mails", "A166": "mails", "A196": "mails", "A121": "mails", "A115": "mails",
  "A235": "files", "A312": "numbers", "A221": "mails", "A186": "files", "A189": "files", "A102": "mails",
  "A451": "person", "A999": "files", "A777": "files"
}

export default function Home() {
  const [logs, setLogs] = useState<TerminalLog[]>([
    { timestamp: new Date().toISOString(), type: "info", message: "BL4CKOPS-OSINT v2.0 INITIALIZED" },
    { timestamp: new Date().toISOString(), type: "success", message: "ALL MODULES LOADED SUCCESSFULLY" },
    { timestamp: new Date().toISOString(), type: "info", message: "SYSTEM STATUS: ONLINE" },
    { timestamp: new Date().toISOString(), type: "info", message: "AWAITING MISSION PARAMETERS..." }
  ])

  const addLog = (type: TerminalLog["type"], message: string, link?: string) => {
    setLogs(prev => [...prev, {
      timestamp: new Date().toISOString(),
      type,
      message,
      link
    }])
  }

  const handleExecuteModule = async (moduleId: string) => {
    const osintModule = MODULE_TO_OSINT[moduleId as keyof typeof MODULE_TO_OSINT] || "files"
    const moduleName = Object.values(MODULES).flat().find(m => m.moduleId === moduleId)?.description || "UNKNOWN"
    
    addLog("info", `[${moduleName}] Module execution started [${moduleId}]`)
    
    try {
      const hostname = typeof window !== 'undefined' ? window.location.hostname : '127.0.0.1'
      const response = await fetch(`http://${hostname}:8000/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          module: osintModule,
          target: "example.com",
          mode: "simulate",
          results_per_query: 3
        })
      })

      const results = await response.json()
      setLogs(prev => [...prev, ...results])
      addLog("success", `[${moduleName}] Execution completed successfully`)
    } catch (error) {
      addLog("error", `[${moduleName}] Execution failed: ${error instanceof Error ? error.message : 'Unknown error'}`)
    }
  }

  const renderModuleButton = (module: typeof MODULES.dump[0]) => (
    <Card
      key={module.moduleId}
      className="bg-[rgb(15,15,15)] border-[rgb(0,255,65)] border-opacity-30 hover:border-opacity-100 transition-all duration-300 p-4 cursor-pointer glow-green hover:glow-green group"
      onClick={() => handleExecuteModule(module.moduleId)}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4 flex-1">
          <div className="text-[rgb(0,255,65)] text-2xl font-bold terminal-text">
            [{module.id}]
          </div>
          <div className="flex flex-col gap-1">
            <div className="flex items-center gap-3">
              <span className="text-[rgb(0,255,65)] font-semibold uppercase tracking-wider">
                {module.name}
              </span>
              <span className="text-[rgb(0,180,45)] text-sm">|</span>
              <span className="text-[rgb(0,180,45)] text-sm">{module.description}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="border border-[rgb(0,255,65)] text-[rgb(0,255,65)] bg-transparent text-xs px-2 py-1 rounded">
                ID: {module.moduleId}
              </span>
              <span className="bg-[rgb(0,255,65)] text-[rgb(10,10,10)] text-xs px-2 py-1 rounded font-bold flex items-center gap-1">
                <Unlock className="w-3 h-3" /> ACTIVATE
              </span>
            </div>
          </div>
        </div>
        <button
          className="bg-[rgb(0,255,65)] text-[rgb(10,10,10)] hover:bg-[rgb(0,200,50)] font-bold uppercase tracking-wider px-4 py-2 rounded text-sm transition-all"
        >
          Execute
        </button>
      </div>
    </Card>
  )

  return (
    <div className="min-h-screen bg-[rgb(10,10,10)] relative overflow-hidden">
      <div className="absolute inset-0 bg-[linear-gradient(rgba(0,255,65,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(0,255,65,0.03)_1px,transparent_1px)] bg-[size:50px_50px]" />
      <div className="absolute inset-0 bg-[linear-gradient(transparent_50%,rgba(0,255,65,0.02)_50%)] bg-[length:100%_4px] pointer-events-none animate-[scan_8s_linear_infinite]" />

      <div className="relative z-10 container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            {/* SVG Logo replacement (no broken image) */}
            <div className="w-20 h-20 rounded-lg border-2 border-[rgb(0,255,65)] flex items-center justify-center bg-[rgb(15,15,15)] glow-green">
              <svg width="60" height="60" viewBox="0 0 100 100" fill="none" stroke="rgb(0,255,65)" strokeWidth="2">
                <rect x="20" y="20" width="60" height="60" rx="5"/>
                <circle cx="50" cy="50" r="20" fill="rgba(0,255,65,0.1)"/>
                <path d="M35 50 L50 35 L65 50 L50 65 Z" fill="rgb(0,255,65)"/>
              </svg>
            </div>
            <div>
              <div className="flex items-center gap-3 mb-1">
                <h1 className="tactical-title text-4xl glow-green-text text-[rgb(0,255,65)]">
                  BL4CKOPS-OSINT
                </h1>
                <div className="flex flex-col items-center gap-0.5">
                  <div className="w-12 h-3 bg-[rgb(220,20,60)] rounded-sm"></div>
                  <div className="w-12 h-3 bg-white rounded-sm"></div>
                </div>
              </div>
              <p className="terminal-text text-sm text-[rgb(0,180,45)]">
                [ OPEN SOURCE INTELLIGENCE TACTICAL FRAMEWORK ] 🇮🇩 MADE IN INDONESIA
              </p>
            </div>
          </div>
          <Card className="bg-[rgb(15,15,15)] border-[rgb(0,255,65)] border-opacity-30 px-4 py-2">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-[rgb(0,255,65)] animate-pulse"></div>
              <span className="terminal-text text-sm">SYSTEM ONLINE</span>
            </div>
          </Card>
        </div>

        {/* Mission Brief */}
        <Card className="bg-[rgb(15,15,15)] border-[rgb(0,255,65)] border-opacity-30 p-6 mb-8 glow-green">
          <div className="flex items-start gap-4">
            <Shield className="w-8 h-8 text-[rgb(0,255,65)] flex-shrink-0 mt-1" />
            <div>
              <h2 className="tactical-title text-xl text-[rgb(0,255,65)] mb-2">
                MISSION BRIEF
              </h2>
              <p className="terminal-text text-sm text-[rgb(0,180,45)] leading-relaxed">
                This tactical OSINT framework provides advanced intelligence gathering capabilities through Google dorking techniques. Select a module below to initiate reconnaissance operations. All modules are operational and ready for deployment.
              </p>
            </div>
          </div>
        </Card>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <Tabs defaultValue="dump" className="w-full">
              <TabsList className="grid w-full grid-cols-3 bg-[rgb(15,15,15)] border border-[rgb(0,255,65)] border-opacity-30 mb-6">
                <TabsTrigger 
                  value="dump"
                  className="terminal-text data-[state=active]:bg-[rgb(0,255,65)] data-[state=active]:text-[rgb(10,10,10)] uppercase tracking-wider"
                >
                  <Database className="w-4 h-4 mr-2" />
                  Data Dumps
                </TabsTrigger>
                <TabsTrigger 
                  value="scrapper"
                  className="terminal-text data-[state=active]:bg-[rgb(0,255,65)] data-[state=active]:text-[rgb(10,10,10)] uppercase tracking-wider"
                >
                  <Search className="w-4 h-4 mr-2" />
                  Scrappers
                </TabsTrigger>
                <TabsTrigger 
                  value="advanced"
                  className="terminal-text data-[state=active]:bg-[rgb(0,255,65)] data-[state=active]:text-[rgb(10,10,10)] uppercase tracking-wider"
                >
                  <User className="w-4 h-4 mr-2" />
                  Advanced
                </TabsTrigger>
              </TabsList>

              {/* Data Dumps Tab */}
              <TabsContent value="dump" className="space-y-3">
                <div className="bg-[rgb(15,15,15)] border border-[rgb(0,255,65)] border-opacity-20 p-3 mb-4">
                  <h3 className="terminal-text uppercase tracking-wider text-[rgb(0,255,65)] font-bold">
                    SELECT MODULE
                  </h3>
                </div>
                {MODULES.dump.map(module => renderModuleButton(module))}
              </TabsContent>

              {/* Scrappers Tab */}
              <TabsContent value="scrapper" className="space-y-3">
                <div className="bg-[rgb(15,15,15)] border border-[rgb(0,255,65)] border-opacity-20 p-3 mb-4">
                  <h3 className="terminal-text uppercase tracking-wider text-[rgb(0,255,65)] font-bold">
                    SELECT MODULE
                  </h3>
                </div>
                {MODULES.scrapper.map(module => renderModuleButton(module))}
              </TabsContent>

              {/* Advanced Tab */}
              <TabsContent value="advanced" className="space-y-3">
                <div className="bg-[rgb(15,15,15)] border border-[rgb(0,255,65)] border-opacity-20 p-3 mb-4">
                  <h3 className="terminal-text uppercase tracking-wider text-[rgb(0,255,65)] font-bold">
                    ADVANCED MODULES
                  </h3>
                </div>
                {MODULES.advanced.map(module => renderModuleButton(module))}
              </TabsContent>
            </Tabs>
          </div>

          {/* Terminal Panel */}
          <div>
            <OSINTTerminal logs={logs} />
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 text-center">
          <p className="terminal-text text-xs text-[rgb(0,180,45)]">
            [ CLASSIFIED ] BL4CKOPS-OSINT v2.0 | FOR AUTHORIZED PERSONNEL ONLY
          </p>
        </div>
      </div>
    </div>
  )
}