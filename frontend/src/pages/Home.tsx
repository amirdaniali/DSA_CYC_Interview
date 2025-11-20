// Home.tsx
import { useEffect, useState } from "react";
import { listSessions } from "@/lib/sessionApi";
import type { Session } from "@/lib/types";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Link } from "react-router";
import { useAuth } from "@/context/AuthContext";

export default function Home() {
    const [sessions, setSessions] = useState<Session[]>([]);
    const { user } = useAuth();

    useEffect(() => {
        listSessions().then(setSessions).catch(console.error);
    }, []);

    return (
        <div className="space-y-8">
            <h1 className="text-2xl font-bold">Upcoming Interview Sessions</h1>
            <div>
                {user ? <h2>Hi {user.fullname}</h2> : <p></p>}
            </div>
            <div className="grid gap-4 sm:grid-cols-2">
                {sessions.map((s) => (
                    <Card key={s.id} className="p-4">
                        <div>{s.date}</div>
                        <div>Capacity: {s.capacity} • Queue: {s.signup_count}</div>
                    </Card>
                ))}
            </div>
            {user?.isAdmin && (
                <div className="pt-8 border-t">
                    <Link to="/manage">
                        <Button variant="outline">Go to Admin Panel</Button>
                    </Link>
                </div>
            )}
        </div>
    );
}
