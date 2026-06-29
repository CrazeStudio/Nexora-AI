import { Link, useLocation } from "wouter";
import { BrainCircuit, MessageSquare, Database } from "lucide-react";

export function Layout({ children }: { children: React.ReactNode }) {
  const [location] = useLocation();

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col md:flex-row">
      <nav className="w-full md:w-64 border-b md:border-b-0 md:border-r border-border bg-card flex flex-col">
        <div className="p-6 flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center">
            <BrainCircuit className="w-5 h-5 text-primary" />
          </div>
          <span className="font-semibold text-lg tracking-tight">NexoraAI</span>
        </div>
        
        <div className="px-4 pb-6 flex-1 flex flex-col gap-2">
          <Link href="/">
            <div className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors cursor-pointer ${
              location === "/" 
                ? "bg-primary text-primary-foreground font-medium shadow-sm" 
                : "text-muted-foreground hover:bg-muted hover:text-foreground"
            }`}>
              <MessageSquare className="w-4 h-4" />
              <span>Chat</span>
            </div>
          </Link>
          
          <Link href="/memory">
            <div className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors cursor-pointer ${
              location === "/memory" 
                ? "bg-primary text-primary-foreground font-medium shadow-sm" 
                : "text-muted-foreground hover:bg-muted hover:text-foreground"
            }`}>
              <Database className="w-4 h-4" />
              <span>Memory Vault</span>
            </div>
          </Link>
        </div>
      </nav>
      
      <main className="flex-1 bg-background flex flex-col h-[100dvh] overflow-hidden relative">
        {children}
      </main>
    </div>
  );
}
