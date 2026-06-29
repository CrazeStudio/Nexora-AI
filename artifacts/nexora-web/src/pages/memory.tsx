import { Layout } from "@/components/layout";
import { useSession } from "@/hooks/use-session";
import { useGetMemory, useRememberFact, useClearMemory, getGetMemoryQueryKey } from "@workspace/api-client-react";
import { useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Database, Trash2, Plus, AlertCircle, DatabaseZap } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

export default function MemoryPage() {
  const { sessionId } = useSession();
  const queryClient = useQueryClient();
  const [newFact, setNewFact] = useState("");

  const { data, isLoading, error } = useGetMemory(
    { sessionId: sessionId || undefined },
    { query: { enabled: !!sessionId, queryKey: getGetMemoryQueryKey({ sessionId: sessionId || undefined }) } }
  );

  const rememberFact = useRememberFact();
  const clearMemory = useClearMemory();

  const handleAddFact = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newFact.trim()) return;

    rememberFact.mutate(
      { data: { fact: newFact, sessionId } },
      {
        onSuccess: () => {
          setNewFact("");
          queryClient.invalidateQueries({ queryKey: getGetMemoryQueryKey({ sessionId: sessionId || undefined }) });
        }
      }
    );
  };

  const handleClear = () => {
    if (!sessionId) return;
    if (confirm("Are you sure you want to clear all memory? This cannot be undone.")) {
      clearMemory.mutate(
        { params: { sessionId } },
        {
          onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: getGetMemoryQueryKey({ sessionId: sessionId || undefined }) });
          }
        }
      );
    }
  };

  const memories = data?.memories || [];

  return (
    <Layout>
      <div className="flex-1 overflow-y-auto p-6 md:p-10">
        <div className="max-w-4xl mx-auto space-y-8">
          
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h1 className="text-3xl font-semibold tracking-tight mb-2">Memory Vault</h1>
              <p className="text-muted-foreground">Manage everything NexoraAI remembers about this session.</p>
            </div>
            {memories.length > 0 && (
              <Button variant="destructive" size="sm" onClick={handleClear} disabled={clearMemory.isPending} className="self-start md:self-auto gap-2">
                <Trash2 className="w-4 h-4" />
                Clear Memory
              </Button>
            )}
          </div>

          <Card className="border-border shadow-sm">
            <CardHeader className="bg-muted/30 border-b border-border/50">
              <CardTitle className="text-lg flex items-center gap-2">
                <Plus className="w-5 h-5 text-primary" />
                Add Knowledge
              </CardTitle>
              <CardDescription>Explicitly teach NexoraAI a new fact for this session.</CardDescription>
            </CardHeader>
            <CardContent className="p-6">
              <form onSubmit={handleAddFact} className="flex gap-3">
                <Input 
                  value={newFact}
                  onChange={(e) => setNewFact(e.target.value)}
                  placeholder="e.g. My favorite color is midnight blue..."
                  className="flex-1 bg-background"
                  disabled={rememberFact.isPending || !sessionId}
                />
                <Button type="submit" disabled={!newFact.trim() || rememberFact.isPending || !sessionId} className="gap-2">
                  <DatabaseZap className="w-4 h-4" />
                  Remember
                </Button>
              </form>
              {!sessionId && (
                <p className="text-sm text-destructive mt-3 font-medium flex items-center gap-1">
                  <AlertCircle className="w-4 h-4" />
                  Start a chat first to initialize a session.
                </p>
              )}
            </CardContent>
          </Card>

          <div className="space-y-4">
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <Database className="w-5 h-5 text-muted-foreground" />
              Stored Facts
            </h2>
            
            {isLoading ? (
              <div className="space-y-3">
                {[1, 2, 3].map(i => (
                  <div key={i} className="h-16 rounded-xl bg-muted/50 animate-pulse border border-border" />
                ))}
              </div>
            ) : error ? (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>Failed to load memories. Please try again.</AlertDescription>
              </Alert>
            ) : memories.length === 0 ? (
              <Card className="bg-muted/30 border-dashed">
                <CardContent className="flex flex-col items-center justify-center py-12 text-center">
                  <div className="w-12 h-12 rounded-full bg-background border border-border flex items-center justify-center mb-4">
                    <Database className="w-5 h-5 text-muted-foreground" />
                  </div>
                  <h3 className="text-lg font-medium mb-1">Memory is empty</h3>
                  <p className="text-muted-foreground text-sm max-w-sm">NexoraAI hasn't learned any persistent facts in this session yet.</p>
                </CardContent>
              </Card>
            ) : (
              <div className="grid gap-3">
                {memories.map((memory, i) => (
                  <Card key={i} className="group hover:border-primary/30 transition-colors bg-card shadow-sm">
                    <CardContent className="p-4 flex gap-4 items-start">
                      <div className="w-6 h-6 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                        <span className="text-xs font-mono text-primary font-medium">{i + 1}</span>
                      </div>
                      <p className="text-sm leading-relaxed">{memory}</p>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
}
