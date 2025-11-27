"use client"

import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Lock, Unlock } from "lucide-react"

interface OSINTModuleProps {
  id: string
  name: string
  description: string
  moduleId: string
  status: "ACTIVATE" | "DEACTIVATE"
  onClick: () => void
}

export function OSINTModule({ id, name, description, moduleId, status, onClick }: OSINTModuleProps) {
  return (
    <Card 
      className="bg-[rgb(15,15,15)] border-[rgb(0,255,65)] border-opacity-30 hover:border-opacity-100 transition-all duration-300 p-4 cursor-pointer glow-green hover:glow-green group"
      onClick={onClick}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4 flex-1">
          <div className="text-[rgb(0,255,65)] text-2xl font-bold terminal-text">
            [{id}]
          </div>
          <div className="flex flex-col gap-1">
            <div className="flex items-center gap-3">
              <span className="text-[rgb(0,255,65)] font-semibold uppercase tracking-wider">
                {name}
              </span>
              <span className="text-[rgb(0,180,45)] text-sm">|</span>
              <span className="text-[rgb(0,180,45)] text-sm">{description}</span>
            </div>
            <div className="flex items-center gap-2">
              <Badge 
                variant="outline" 
                className="border-[rgb(0,255,65)] text-[rgb(0,255,65)] bg-transparent text-xs"
              >
                ID: {moduleId}
              </Badge>
              <Badge 
                variant={status === "ACTIVATE" ? "default" : "secondary"}
                className={`${
                  status === "ACTIVATE" 
                    ? "bg-[rgb(0,255,65)] text-[rgb(10,10,10)]" 
                    : "bg-[rgb(20,20,20)] text-[rgb(0,180,45)]"
                } text-xs font-bold`}
              >
                {status === "ACTIVATE" ? (
                  <span className="flex items-center gap-1">
                    <Unlock className="w-3 h-3" /> {status}
                  </span>
                ) : (
                  <span className="flex items-center gap-1">
                    <Lock className="w-3 h-3" /> {status}
                  </span>
                )}
              </Badge>
            </div>
          </div>
        </div>
        <Button 
          size="sm"
          className="bg-[rgb(0,255,65)] text-[rgb(10,10,10)] hover:bg-[rgb(0,200,50)] font-bold uppercase tracking-wider"
        >
          Execute
        </Button>
      </div>
    </Card>
  )
}
