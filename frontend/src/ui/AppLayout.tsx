import { Outlet, Link, useLocation } from "react-router";
import { Button } from "@/components/ui/button";


export default function AppLayout() {
  const loc = useLocation();
  return (
    <div className="min-h-screen bg-neutral-50">
      <header className="border-b bg-white">
        <div className="mx-auto max-w-5xl px-4 py-3 flex items-center justify-between">
          <Link to="/" className="font-semibold tracking-tight">DSA Interviews Queue</Link>
          <nav className="flex gap-3">
            <Link to="/sessions"><Button variant={loc.pathname==="/sessions"?"default":"ghost"}>Sessions</Button></Link>
            <Link to="/admin/sessions"><Button variant={loc.pathname==="/admin/sessions"?"default":"ghost"}>Admin</Button></Link>
            <Link to="/login"><Button variant={loc.pathname==="/login"?"default":"outline"}>Login</Button></Link>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-5xl px-4 py-8">
        <Outlet />
      </main>
    </div>
  );
}
