"use client"

import { useState } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Loader2 } from "lucide-react"

interface OSINTExecutionDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  moduleId: string
  moduleName: string
  moduleType: "dump" | "scrapper" | "advanced"
  onExecute: (params: any) => Promise<void>
}

export function OSINTExecutionDialog({
  open,
  onOpenChange,
  moduleId,
  moduleName,
  moduleType,
  onExecute
}: OSINTExecutionDialogProps) {
  const [loading, setLoading] = useState(false)
  const [target, setTarget] = useState("")
  const [countryCode, setCountryCode] = useState("")
  const [name, setName] = useState("")
  const [surname, setSurname] = useState("")
  const [phone, setPhone] = useState("")
  const [dork, setDork] = useState("")

  const handleExecute = async () => {
    setLoading(true)
    try {
      const params: any = { moduleId }

      // Add parameters based on module type
      if (moduleType === "scrapper") {
        params.target = target
        if (moduleId === "A312") {
          params.countryCode = countryCode
        }
      } else if (moduleType === "advanced") {
        if (moduleId === "A451") {
          params.name = name
          params.surname = surname
          params.phone = phone
        } else if (moduleId === "A999") {
          params.target = target
        } else if (moduleId === "A777") {
          params.dork = dork
        }
      }

      await onExecute(params)
      onOpenChange(false)
      
      // Reset form
      setTarget("")
      setCountryCode("")
      setName("")
      setSurname("")
      setPhone("")
      setDork("")
    } catch (error) {
      console.error("Execution error:", error)
    } finally {
      setLoading(false)
    }
  }

  const renderInputs = () => {
    if (moduleType === "dump") {
      return (
        <div className="space-y-4">
          <p className="terminal-text text-sm text-[rgb(0,180,45)]">
            This module will execute automatically. No additional parameters required.
          </p>
        </div>
      )
    }

    if (moduleType === "scrapper") {
      return (
        <div className="space-y-4">
          <div>
            <Label htmlFor="target" className="terminal-text text-[rgb(0,255,65)]">
              Target Domain *
            </Label>
            <Input
              id="target"
              placeholder="example"
              value={target}
              onChange={(e) => setTarget(e.target.value)}
              className="bg-[rgb(20,20,20)] border-[rgb(0,255,65)] border-opacity-30 text-[rgb(0,255,65)] terminal-text"
              required
            />
            <p className="text-xs text-[rgb(0,180,45)] mt-1">Enter domain without .com</p>
          </div>

          {moduleId === "A312" && (
            <div>
              <Label htmlFor="countryCode" className="terminal-text text-[rgb(0,255,65)]">
                Country Code *
              </Label>
              <Input
                id="countryCode"
                placeholder="+62"
                value={countryCode}
                onChange={(e) => setCountryCode(e.target.value)}
                className="bg-[rgb(20,20,20)] border-[rgb(0,255,65)] border-opacity-30 text-[rgb(0,255,65)] terminal-text"
                required
              />
            </div>
          )}
        </div>
      )
    }

    if (moduleType === "advanced") {
      if (moduleId === "A451") {
        return (
          <div className="space-y-4">
            <div>
              <Label htmlFor="name" className="terminal-text text-[rgb(0,255,65)]">
                Name *
              </Label>
              <Input
                id="name"
                placeholder="John"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="bg-[rgb(20,20,20)] border-[rgb(0,255,65)] border-opacity-30 text-[rgb(0,255,65)] terminal-text"
                required
              />
            </div>
            <div>
              <Label htmlFor="surname" className="terminal-text text-[rgb(0,255,65)]">
                Surname (Optional)
              </Label>
              <Input
                id="surname"
                placeholder="Doe"
                value={surname}
                onChange={(e) => setSurname(e.target.value)}
                className="bg-[rgb(20,20,20)] border-[rgb(0,255,65)] border-opacity-30 text-[rgb(0,255,65)] terminal-text"
              />
            </div>
            <div>
              <Label htmlFor="phone" className="terminal-text text-[rgb(0,255,65)]">
                Phone Number (Optional)
              </Label>
              <Input
                id="phone"
                placeholder="+1234567890"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                className="bg-[rgb(20,20,20)] border-[rgb(0,255,65)] border-opacity-30 text-[rgb(0,255,65)] terminal-text"
              />
            </div>
          </div>
        )
      } else if (moduleId === "A999") {
        return (
          <div className="space-y-4">
            <div>
              <Label htmlFor="target" className="terminal-text text-[rgb(0,255,65)]">
                Target Domain *
              </Label>
              <Input
                id="target"
                placeholder="example"
                value={target}
                onChange={(e) => setTarget(e.target.value)}
                className="bg-[rgb(20,20,20)] border-[rgb(0,255,65)] border-opacity-30 text-[rgb(0,255,65)] terminal-text"
                required
              />
              <p className="text-xs text-[rgb(0,180,45)] mt-1">Enter domain without .com</p>
            </div>
          </div>
        )
      } else if (moduleId === "A777") {
        return (
          <div className="space-y-4">
            <div>
              <Label htmlFor="dork" className="terminal-text text-[rgb(0,255,65)]">
                Custom Dork Query *
              </Label>
              <Input
                id="dork"
                placeholder="site:example.com filetype:pdf"
                value={dork}
                onChange={(e) => setDork(e.target.value)}
                className="bg-[rgb(20,20,20)] border-[rgb(0,255,65)] border-opacity-30 text-[rgb(0,255,65)] terminal-text"
                required
              />
              <p className="text-xs text-[rgb(0,180,45)] mt-1">Enter your custom Google dork query</p>
            </div>
          </div>
        )
      }
    }

    return null
  }

  const canExecute = () => {
    if (moduleType === "dump") return true
    if (moduleType === "scrapper") {
      if (moduleId === "A312") return target && countryCode
      return target
    }
    if (moduleType === "advanced") {
      if (moduleId === "A451") return name
      if (moduleId === "A999") return target
      if (moduleId === "A777") return dork
    }
    return false
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="bg-[rgb(15,15,15)] border-[rgb(0,255,65)] border-opacity-50 text-[rgb(0,255,65)] max-w-md">
        <DialogHeader>
          <DialogTitle className="tactical-title text-[rgb(0,255,65)] text-xl">
            EXECUTE: {moduleName}
          </DialogTitle>
          <DialogDescription className="terminal-text text-[rgb(0,180,45)]">
            Module ID: {moduleId} | Status: READY
          </DialogDescription>
        </DialogHeader>

        <div className="mt-4">
          {renderInputs()}
        </div>

        <div className="flex gap-3 mt-6">
          <Button
            onClick={handleExecute}
            disabled={loading || !canExecute()}
            className="flex-1 bg-[rgb(0,255,65)] text-[rgb(10,10,10)] hover:bg-[rgb(0,200,50)] font-bold uppercase tracking-wider"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                EXECUTING...
              </>
            ) : (
              "EXECUTE"
            )}
          </Button>
          <Button
            onClick={() => onOpenChange(false)}
            variant="outline"
            disabled={loading}
            className="border-[rgb(0,255,65)] text-[rgb(0,255,65)] hover:bg-[rgb(20,20,20)] uppercase tracking-wider"
          >
            CANCEL
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}
