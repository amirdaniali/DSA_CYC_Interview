// src/pages/Home.tsx
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Link } from "react-router";

export default function Home() {
  return (
    <div className="grid gap-6 sm:grid-cols-2">
      <Card className="p-6 space-y-2">
        <h2 className="text-lg font-semibold">Students</h2>
        <p className="text-sm text-neutral-600">Browse sessions and join the queue for a DSA interview practice slot.</p>
        <Link to="/sessions"><Button>View sessions</Button></Link>
      </Card>
      <Card className="p-6 space-y-2">
        <h2 className="text-lg font-semibold">Admins</h2>
        <p className="text-sm text-neutral-600">Create sessions and mark them closed once appointments are set.</p>
        <Link to="/admin/sessions"><Button variant="outline">Manage sessions</Button></Link>
      </Card>
    </div>
  );
}
