// Sessions.tsx
import { useAuth } from "@/context/AuthContext";
import { listSessions } from "@/lib/sessionApi";
import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";


export default function Sessions() {
    const { user } = useAuth();
    const [sessions, setSessions] = useState([]);

    useEffect(() => { listSessions().then(setSessions); }, []);

    return (
        <div className="grid gap-4 sm:grid-cols-2">
            {sessions.map(s => (
                <Card key={s.id} className="p-4">
                    <div>{s.date} {s.start_time} – {s.end_time}</div>
                    <div>Capacity: {s.capacity} • Queue: {s.signup_count}</div>
                    {user && (
                        <Button onClick={() => handleSignup(s.id)}>Join queue</Button>
                    )}
                </Card>
            ))}
        </div>
    );
}
