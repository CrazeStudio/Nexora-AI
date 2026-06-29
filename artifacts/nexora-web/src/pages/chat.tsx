import { useSendMessage, useGetSuggestions, getGetSuggestionsQueryKey } from "@workspace/api-client-react";
import { useSession } from "@/hooks/use-session";
import { useState, useRef, useEffect } from "react";
import { Layout } from "@/components/layout";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Search, Sparkles, Send, BrainCircuit, ExternalLink } from "lucide-react";


interface Message {
  id: string;
  role: "user" | "assistant";
  text: string;
  source: string;
  searchResults?: { title: string; url: string; snippet: string }[] | null;
  time: string;
}

export default function ChatPage() {
  const { sessionId, ensureSession, saveSession } = useSession();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const { data: suggestions } = useGetSuggestions({
    query: { queryKey: getGetSuggestionsQueryKey() }
  });

  const sendMessage = useSendMessage();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, sendMessage.isPending]);

  const handleSend = (text: string) => {
    if (!text.trim()) return;

    const currentSession = ensureSession();
    
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      text,
      source: "user",
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMessage]);
    setInput("");

    sendMessage.mutate({
      data: { message: text, sessionId: currentSession }
    }, {
      onSuccess: (resp) => {
        if (resp.sessionId) {
          saveSession(resp.sessionId);
        }
        
        const assistantMessage: Message = {
          id: crypto.randomUUID(),
          role: "assistant",
          text: resp.reply,
          source: resp.source,
          searchResults: resp.searchResults,
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
        
        setMessages(prev => [...prev, assistantMessage]);
      }
    });
  };

  const getSourceBadge = (source: string) => {
    const sourceMap: Record<string, { label: string, icon: any, color: string }> = {
      knowledge: { label: "Knowledge", icon: BrainCircuit, color: "bg-primary/10 text-primary border-primary/20" },
      search: { label: "Search", icon: Search, color: "bg-secondary/10 text-secondary border-secondary/20" },
      math: { label: "Math", icon: Sparkles, color: "bg-accent text-accent-foreground border-accent-foreground/20" },
      dataset: { label: "Dataset", icon: BrainCircuit, color: "bg-muted text-muted-foreground border-border" },
      example: { label: "Example", icon: Sparkles, color: "bg-primary/10 text-primary border-primary/20" },
      social: { label: "Social", icon: Sparkles, color: "bg-secondary/10 text-secondary border-secondary/20" },
      fallback: { label: "Fallback", icon: BrainCircuit, color: "bg-muted text-muted-foreground border-border" },
    };

    const config = sourceMap[source] || { label: source, icon: Sparkles, color: "bg-muted text-muted-foreground border-border" };
    const Icon = config.icon;

    return (
      <Badge variant="outline" className={`text-xs font-normal gap-1 px-2 py-0.5 ${config.color}`}>
        <Icon className="w-3 h-3" />
        {config.label}
      </Badge>
    );
  };

  return (
    <Layout>
      <div className="flex flex-col h-[calc(100vh-4rem)] max-w-4xl mx-auto w-full">
        {messages.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center p-8 animate-in fade-in zoom-in duration-500">
            <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mb-6 shadow-sm">
              <BrainCircuit className="w-8 h-8 text-primary" />
            </div>
            <h1 className="text-3xl font-semibold mb-2 text-foreground tracking-tight">NexoraAI</h1>
            <p className="text-muted-foreground mb-12 text-center max-w-md">
              A clever colleague who always has an answer ready. Ask me anything from my built-in knowledge.
            </p>
            
            <div className="w-full max-w-2xl grid grid-cols-1 md:grid-cols-2 gap-3">
              {suggestions?.suggestions.map((suggestion, i) => (
                <Card 
                  key={i} 
                  className="p-4 cursor-pointer hover:border-primary/50 hover:bg-primary/5 transition-all active:scale-[0.98] group"
                  onClick={() => handleSend(suggestion)}
                >
                  <p className="text-sm font-medium text-foreground group-hover:text-primary transition-colors">
                    {suggestion}
                  </p>
                </Card>
              ))}
            </div>
          </div>
        ) : (
          <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6">
            {messages.map((msg, i) => (
              <div 
                key={msg.id} 
                className={`flex flex-col ${msg.role === "user" ? "items-end" : "items-start"} animate-in slide-in-from-bottom-2 fade-in duration-300`}
                style={{ animationFillMode: "both", animationDelay: `${i * 50}ms` }}
              >
                <div className="flex items-center gap-2 mb-1.5 px-1">
                  {msg.role === "assistant" && getSourceBadge(msg.source)}
                  <span className="text-[10px] text-muted-foreground font-mono">{msg.time}</span>
                </div>
                
                <div 
                  className={`max-w-[85%] rounded-2xl px-5 py-3.5 shadow-sm ${
                    msg.role === "user" 
                      ? "bg-foreground text-background rounded-tr-sm" 
                      : "bg-card border border-border rounded-tl-sm text-foreground"
                  }`}
                >
                  <div className="whitespace-pre-wrap text-[15px] leading-relaxed">
                    {msg.text}
                  </div>
                  
                  {msg.searchResults && msg.searchResults.length > 0 && (
                    <div className="mt-4 pt-4 border-t border-border/50 space-y-3">
                      <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Sources</p>
                      <div className="grid gap-2">
                        {msg.searchResults.map((result, idx) => (
                          <a 
                            key={idx} 
                            href={result.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="block p-3 rounded-lg border border-border bg-muted/30 hover:bg-muted/50 hover:border-primary/30 transition-colors group"
                          >
                            <div className="flex items-start justify-between gap-2 mb-1">
                              <h4 className="text-sm font-medium line-clamp-1 group-hover:text-primary transition-colors">{result.title}</h4>
                              <ExternalLink className="w-3.5 h-3.5 text-muted-foreground flex-shrink-0 group-hover:text-primary transition-colors" />
                            </div>
                            <p className="text-xs text-muted-foreground line-clamp-2">{result.snippet}</p>
                          </a>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}
            
            {sendMessage.isPending && (
              <div className="flex flex-col items-start animate-in fade-in duration-300">
                <div className="flex items-center gap-2 mb-1 px-1">
                  <span className="text-[10px] text-muted-foreground font-mono">Thinking...</span>
                </div>
                <div className="bg-card border border-border rounded-2xl rounded-tl-sm px-5 py-4 shadow-sm flex items-center gap-1.5">
                  <div className="w-1.5 h-1.5 rounded-full bg-primary/60 animate-bounce" style={{ animationDelay: "0ms" }} />
                  <div className="w-1.5 h-1.5 rounded-full bg-primary/60 animate-bounce" style={{ animationDelay: "150ms" }} />
                  <div className="w-1.5 h-1.5 rounded-full bg-primary/60 animate-bounce" style={{ animationDelay: "300ms" }} />
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}

        <div className="p-4 md:p-6 bg-background/80 backdrop-blur-md border-t border-border sticky bottom-0">
          <form 
            onSubmit={(e) => {
              e.preventDefault();
              if (!input.trim()) {
                inputRef.current?.classList.add("animate-shake");
                setTimeout(() => inputRef.current?.classList.remove("animate-shake"), 500);
                return;
              }
              handleSend(input);
            }}
            className="relative flex items-center"
          >
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask NexoraAI anything..."
              className="w-full pl-5 pr-14 py-4 rounded-xl border border-input bg-card text-base shadow-sm focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all placeholder:text-muted-foreground"
              disabled={sendMessage.isPending}
            />
            <Button 
              type="submit" 
              size="icon" 
              className="absolute right-2 h-10 w-10 rounded-lg shadow-sm"
              disabled={!input.trim() || sendMessage.isPending}
            >
              <Send className="w-4 h-4 ml-0.5" />
            </Button>
          </form>
          <div className="text-center mt-3">
            <p className="text-[11px] text-muted-foreground font-medium">NexoraAI can make mistakes. Verify important information.</p>
          </div>
        </div>
      </div>
    </Layout>
  );
}
