// src/pages/Sessions.tsx
import { useEffect, useState } from "react";
import { listSessions } from "@/lib/sessionApi";
import { createSignup } from "@/lib/signupApi";
import type { Session } from "@/lib/types";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function Sessions() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [lcLevel, setLcLevel] = useState<"easy"|"medium"| "hard" | "none"|null>(null);
  const [discord, setDiscord] = useState("");

  useEffect(() => {
    listSessions().then(setSessions).catch(console.error);
  }, []);

  const handleSignup = async (sessionId: number) => {
    await createSignup({
      session: sessionId,
      lc_level: lcLevel === "none" ? null : lcLevel,
      discord_username: discord || null,
      status: "active",
    });
    // reflect in UI minimally
    alert("Signed up! You’re in the queue.");
  };

  return (
    <div className="space-y-6">
      <div className="rounded-lg border bg-white p-4">
        <div className="grid sm:grid-cols-3 gap-4">
          <div>
            <Label>LeetCode level</Label>
            <Select onValueChange={(v)=> setLcLevel(v as any)}>
              <SelectTrigger><SelectValue placeholder="Select level"/></SelectTrigger>
              <SelectContent>
                <SelectItem value="easy">Easy</SelectItem>
                <SelectItem value="medium">Medium</SelectItem>
                <SelectItem value="hard">Hard</SelectItem>
                <SelectItem value="none">Prefer not to say</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="sm:col-span-2">
            <Label>Discord username (optional)</Label>
            <Input placeholder="e.g., algo_master#1234" value={discord} onChange={e=> setDiscord(e.target.value)} />
          </div>
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        {sessions.filter(s=> s.is_active !== false).map(s => (
          <Card key={s.id} className="p-4 flex flex-col gap-2">
            <div className="text-sm text-neutral-500">{s.date}</div>
            <div className="font-medium">
              {s.start_time ? s.start_time.slice(0,5) : "TBD"} — {s.end_time ? s.end_time.slice(0,5) : "TBD"}
            </div>
            <div className="text-sm text-neutral-600">
              Capacity: {s.capacity ?? "—"} • In queue: {s.signup_count}
            </div>
            <div className="mt-2">
              <Button onClick={() => handleSignup(s.id)}>Join queue</Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
