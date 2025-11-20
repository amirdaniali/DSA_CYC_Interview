import { useEffect, useState } from "react";
import { listSessions, updateSession, deleteSession, createSession } from "@/lib/sessionApi"; // <-- make sure createSession is exported
import type { Session } from "@/lib/types";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

import { useAuth } from "@/context/AuthContext";
import { Navigate } from "react-router"; // <-- use react-router-dom

export default function AdminSessions() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [newSession, setNewSession] = useState({
    date: "",
    start_time: "",
    end_time: "",
    capacity: 5,
  });

  const load = async () => {
    const data = await listSessions();
    setSessions(data);
  };
  useEffect(() => {
    load();
  }, []);

  const { user } = useAuth();
  if (!user?.isAdmin) return <Navigate to="/" />;

  const add = async () => {
    try {
      const payload = {
        date: newSession.date,
        start_time: newSession.start_time || null,
        end_time: newSession.end_time || null,
        capacity: newSession.capacity,
        is_active: true,
      };
      await createSession(payload);
      await load();
      setNewSession({ date: "", start_time: "", end_time: "", capacity: 5 });
    } catch (err) {
      console.error("Error creating session:", err);
    }
  };

  const closeSession = async (id: number) => {
    await updateSession(id, { is_active: false });
    await load();
  };

  const reopenSession = async (id: number) => {
    await updateSession(id, { is_active: true });
    await load();
  };

  return (
    <div className="space-y-8">
      <Card className="p-4">
        <div className="grid sm:grid-cols-4 gap-4">
          <div>
            <Label>Date</Label>
            <Input
              type="date"
              value={newSession.date}
              onChange={(e) =>
                setNewSession((s) => ({ ...s, date: e.target.value }))
              }
            />
          </div>
          <div>
            <Label>Start time</Label>
            <Input
              type="time"
              value={newSession.start_time}
              onChange={(e) =>
                setNewSession((s) => ({ ...s, start_time: e.target.value }))
              }
            />
          </div>
          <div>
            <Label>End time</Label>
            <Input
              type="time"
              value={newSession.end_time}
              onChange={(e) =>
                setNewSession((s) => ({ ...s, end_time: e.target.value }))
              }
            />
          </div>
          <div>
            <Label>Capacity</Label>
            <Input
              type="number"
              min={0}
              value={newSession.capacity}
              onChange={(e) =>
                setNewSession((s) => ({
                  ...s,
                  capacity: Number(e.target.value),
                }))
              }
            />
          </div>
        </div>
        <div className="mt-4">
          <Button onClick={add}>Create session</Button>
        </div>
      </Card>

      <div className="grid gap-4 sm:grid-cols-2">
        {sessions.map((s) => (
          <Card key={s.id} className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm text-neutral-500">{s.date}</div>
                <div className="font-medium">
                  {s.start_time ? s.start_time.slice(0, 5) : "TBD"} —{" "}
                  {s.end_time ? s.end_time.slice(0, 5) : "TBD"}
                </div>
                <div className="text-sm text-neutral-600">
                  Capacity: {s.capacity ?? "—"} • In queue: {s.signup_count}
                </div>
                <div
                  className={`mt-1 inline-block rounded px-2 py-1 text-xs ${s.is_active
                    ? "bg-green-100 text-green-700"
                    : "bg-yellow-100 text-yellow-700"
                    }`}
                >
                  {s.is_active
                    ? "Active (accepting signups)"
                    : "Closed / Set"}
                </div>
              </div>
              <div className="flex gap-2">
                {s.is_active ? (
                  <Button variant="outline" onClick={() => closeSession(s.id)}>
                    Close
                  </Button>
                ) : (
                  <Button variant="outline" onClick={() => reopenSession(s.id)}>
                    Reopen
                  </Button>
                )}
                <Button
                  variant="destructive"
                  onClick={() => deleteSession(s.id).then(load)}
                >
                  Delete
                </Button>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
