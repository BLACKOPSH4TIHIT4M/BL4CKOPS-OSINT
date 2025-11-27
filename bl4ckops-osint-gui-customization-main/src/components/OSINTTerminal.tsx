"use client"

import { useEffect, useState } from "react"

interface TerminalLog {
  timestamp: string
  type: "info" | "success" | "error" | "result"
  message: string
  link?: string
}

interface OSINTTerminalProps {
  logs?: TerminalLog[]
}

export function OSINTTerminal({ logs = [] }: OSINTTerminalProps) {
  const [internalLogs, setInternalLogs] = useState<TerminalLog[]>(logs)
  const [moduleName, setModuleName] = useState("files")
  const [target, setTarget] = useState("")
  const [running, setRunning] = useState(false)
  const [resultsPerQuery, setResultsPerQuery] = useState(5)
  const [pauseSeconds, setPauseSeconds] = useState(2)

  useEffect(() => {
    if (logs && logs.length > 0) setInternalLogs(logs)
  }, [logs])

  const defaultLogs: TerminalLog[] = [
    { timestamp: new Date().toISOString(), type: "info", message: "BL4CKOPS-OSINT v2.0 INITIALIZED" },
    { timestamp: new Date().toISOString(), type: "success", message: "ALL MODULES LOADED SUCCESSFULLY" },
    { timestamp: new Date().toISOString(), type: "info", message: "SYSTEM STATUS: ONLINE" },
    { timestamp: new Date().toISOString(), type: "info", message: "AWAITING MISSION PARAMETERS..." }
  ]

  const displayLogs = internalLogs.length > 0 ? internalLogs : defaultLogs

  const getLogColor = (type: string) => {
    switch (type) {
      case "success":
        return "text-[rgb(0,255,65)]"
      case "error":
        return "text-[rgb(255,50,50)]"
      case "result":
        return "text-[rgb(100,200,255)]"
      default:
        return "text-[rgb(0,180,45)]"
    }
  }

  const handleRun = async () => {
    if (!target.trim()) {
      setInternalLogs(prev => [...prev, {
        timestamp: new Date().toISOString(),
        type: "error",
        message: "ERROR: Target cannot be empty"
      }])
      return
    }

    setRunning(true)
    setInternalLogs(prev => [...prev, {
      timestamp: new Date().toISOString(),
      type: "info",
      message: `[${moduleName.toUpperCase()}] Starting scan for target: ${target}`
    }])

    try {
      const hostname = typeof window !== 'undefined' ? window.location.hostname : '127.0.0.1'
      const backendUrl = `http://${hostname}:8000/run`
      
      const response = await fetch(backendUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          module: moduleName,
          target: target,
          mode: "simulate",
          results_per_query: resultsPerQuery,
          pause_seconds: pauseSeconds
        })
      })

      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      
      const results = await response.json()
      setInternalLogs(prev => [...prev, ...results])
    } catch (error) {
      setInternalLogs(prev => [...prev, {
        timestamp: new Date().toISOString(),
        type: "error",
        message: `ERROR: ${error instanceof Error ? error.message : 'Unknown error'}`
      }])
    } finally {
      setRunning(false)
    }
  }

  const handleClear = () => {
    setInternalLogs([])
  }

  return (
    <div className="w-full h-full flex flex-col" style={{
      backgroundColor: 'rgb(15,15,15)',
      borderRadius: '8px',
      border: '2px solid rgb(0,255,65)',
      boxShadow: '0 0 20px rgba(0,255,65,0.3), inset 0 0 10px rgba(0,255,65,0.1)',
      overflow: 'hidden'
    }}>
      {/* Header with inline SVG icon */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
        padding: '16px',
        borderBottom: '2px solid rgba(0,255,65,0.3)',
        backgroundColor: 'rgba(0,255,65,0.05)'
      }}>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="rgb(0,255,65)" strokeWidth="2">
          <polyline points="4 17 10 3 20 21 10 13"></polyline>
        </svg>
        <h3 style={{
          fontSize: '14px',
          fontWeight: 'bold',
          color: 'rgb(0,255,65)',
          letterSpacing: '2px',
          fontFamily: 'monospace',
          margin: 0
        }}>
          OPERATION TERMINAL
        </h3>
        <div style={{
          marginLeft: 'auto',
          width: '12px',
          height: '12px',
          borderRadius: '50%',
          backgroundColor: 'rgb(0,255,65)',
          animation: 'pulse 1.5s infinite'
        }} />
      </div>

      {/* Terminal output area */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: '16px',
        backgroundColor: 'rgb(10,10,10)',
        fontFamily: 'monospace',
        fontSize: '12px',
        lineHeight: '1.6'
      }}>
        {displayLogs.map((log, index) => (
          <div key={index} style={{ marginBottom: '8px' }}>
            <div style={{
              display: 'flex',
              gap: '8px',
              alignItems: 'flex-start'
            }}>
              <span style={{
                color: 'rgb(0,100,25)',
                whiteSpace: 'nowrap',
                flexShrink: 0
              }}>
                [{new Date(log.timestamp).toLocaleTimeString()}]
              </span>
              <span style={{ color: getLogColor(log.type), wordBreak: 'break-word' }}>
                {log.message}
              </span>
            </div>
            {log.link && (
              <a
                href={log.link}
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  color: 'rgb(100,200,255)',
                  textDecoration: 'none',
                  marginLeft: '160px',
                  wordBreak: 'break-word',
                  display: 'block'
                }}
                onMouseEnter={e => (e.currentTarget.style.textDecoration = 'underline')}
                onMouseLeave={e => (e.currentTarget.style.textDecoration = 'none')}
              >
                {log.link}
              </a>
            )}
          </div>
        ))}
      </div>

      {/* Control Panel */}
      <div style={{
        borderTop: '2px solid rgba(0,255,65,0.3)',
        backgroundColor: 'rgba(0,255,65,0.02)',
        padding: '16px'
      }}>
        <div style={{ marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div style={{
            width: '8px',
            height: '8px',
            borderRadius: '50%',
            backgroundColor: 'rgb(0,255,65)',
            animation: 'pulse 1.5s infinite'
          }} />
          <span style={{
            fontSize: '11px',
            color: 'rgb(0,180,45)',
            fontFamily: 'monospace',
            letterSpacing: '1px'
          }}>
            SYSTEM STATUS: READY FOR OPERATION
          </span>
        </div>

        {/* Module & Target Selection */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.5fr', gap: '12px', marginBottom: '12px' }}>
          <div>
            <label style={{
              display: 'block',
              fontSize: '10px',
              color: 'rgb(0,180,45)',
              marginBottom: '4px',
              fontWeight: 'bold',
              letterSpacing: '1px'
            }}>
              MODULE
            </label>
            <select
              value={moduleName}
              onChange={e => setModuleName(e.target.value)}
              style={{
                width: '100%',
                padding: '8px',
                backgroundColor: 'rgb(20,20,20)',
                color: 'rgb(0,255,65)',
                border: '1px solid rgba(0,255,65,0.5)',
                fontSize: '12px',
                fontFamily: 'monospace',
                cursor: 'pointer',
                borderRadius: '4px'
              }}
            >
              <option value="files">📄 FILES</option>
              <option value="mails">✉️ MAILS</option>
              <option value="numbers">📞 NUMBERS</option>
              <option value="person">👤 PERSON</option>
              <option value="deobfuscate">🔓 DEOBFUSCATE</option>
            </select>
          </div>

          <div>
            <label style={{
              display: 'block',
              fontSize: '10px',
              color: 'rgb(0,180,45)',
              marginBottom: '4px',
              fontWeight: 'bold',
              letterSpacing: '1px'
            }}>
              TARGET
            </label>
            <input
              type="text"
              placeholder="domain.com or /path/to/file"
              value={target}
              onChange={e => setTarget(e.target.value)}
              onKeyPress={e => e.key === 'Enter' && handleRun()}
              style={{
                width: '100%',
                padding: '8px',
                backgroundColor: 'rgb(20,20,20)',
                color: 'rgb(0,255,65)',
                border: '1px solid rgba(0,255,65,0.5)',
                fontSize: '12px',
                fontFamily: 'monospace',
                borderRadius: '4px',
                boxSizing: 'border-box'
              }}
            />
          </div>
        </div>

        {/* Query Parameters */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '12px' }}>
          <div>
            <label style={{
              display: 'block',
              fontSize: '10px',
              color: 'rgb(0,180,45)',
              marginBottom: '4px',
              fontWeight: 'bold',
              letterSpacing: '1px'
            }}>
              RESULTS PER QUERY
            </label>
            <input
              type="number"
              min="1"
              max="100"
              value={resultsPerQuery}
              onChange={e => setResultsPerQuery(parseInt(e.target.value) || 5)}
              style={{
                width: '100%',
                padding: '8px',
                backgroundColor: 'rgb(20,20,20)',
                color: 'rgb(0,255,65)',
                border: '1px solid rgba(0,255,65,0.5)',
                fontSize: '12px',
                fontFamily: 'monospace',
                borderRadius: '4px',
                boxSizing: 'border-box'
              }}
            />
          </div>

          <div>
            <label style={{
              display: 'block',
              fontSize: '10px',
              color: 'rgb(0,180,45)',
              marginBottom: '4px',
              fontWeight: 'bold',
              letterSpacing: '1px'
            }}>
              PAUSE BETWEEN QUERIES (sec)
            </label>
            <input
              type="number"
              min="0"
              max="60"
              value={pauseSeconds}
              onChange={e => setPauseSeconds(parseInt(e.target.value) || 0)}
              style={{
                width: '100%',
                padding: '8px',
                backgroundColor: 'rgb(20,20,20)',
                color: 'rgb(0,255,65)',
                border: '1px solid rgba(0,255,65,0.5)',
                fontSize: '12px',
                fontFamily: 'monospace',
                borderRadius: '4px',
                boxSizing: 'border-box'
              }}
            />
          </div>
        </div>

        {/* Action Buttons */}
        <div style={{ display: 'flex', gap: '12px' }}>
          <button
            onClick={handleRun}
            disabled={running}
            style={{
              flex: 1,
              padding: '10px',
              backgroundColor: running ? 'rgba(0,200,50,0.5)' : 'rgb(0,200,50)',
              color: 'rgb(255,255,255)',
              border: '1px solid rgba(0,255,65,0.5)',
              fontSize: '12px',
              fontFamily: 'monospace',
              fontWeight: 'bold',
              borderRadius: '4px',
              cursor: running ? 'not-allowed' : 'pointer',
              transition: 'all 0.3s',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              letterSpacing: '1px'
            }}
            onMouseEnter={e => !running && (e.currentTarget.style.boxShadow = '0 0 15px rgba(0,200,50,0.6)')}
            onMouseLeave={e => (e.currentTarget.style.boxShadow = 'none')}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <polygon points="5 3 19 12 5 21 5 3"></polygon>
            </svg>
            {running ? 'RUNNING...' : 'RUN SCAN'}
          </button>

          <button
            onClick={handleClear}
            disabled={running}
            style={{
              flex: 1,
              padding: '10px',
              backgroundColor: running ? 'rgba(100,200,255,0.5)' : 'rgb(100,200,255)',
              color: 'rgb(10,10,10)',
              border: '1px solid rgba(100,200,255,0.5)',
              fontSize: '12px',
              fontFamily: 'monospace',
              fontWeight: 'bold',
              borderRadius: '4px',
              cursor: running ? 'not-allowed' : 'pointer',
              transition: 'all 0.3s',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              letterSpacing: '1px'
            }}
            onMouseEnter={e => !running && (e.currentTarget.style.boxShadow = '0 0 15px rgba(100,200,255,0.6)')}
            onMouseLeave={e => (e.currentTarget.style.boxShadow = 'none')}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="3 6 5 4 21 4 23 6 23 20 1 20 1 6"></polyline>
            </svg>
            CLEAR LOG
          </button>
        </div>
      </div>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
        
        select, input {
          color-scheme: dark;
        }
        
        select option {
          background-color: rgb(20,20,20);
          color: rgb(0,255,65);
        }
      `}</style>
    </div>
  )
}