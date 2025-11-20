// AppLayout.tsx
import { useAuth } from "@/context/AuthContext";
import { Link, Outlet } from "react-router";
import { Button } from "@/components/ui/button";

export default function AppLayout() {
  const { user, logoutUser } = useAuth();

  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b bg-white">
        <div className="mx-auto max-w-5xl px-4 py-3 flex items-center justify-between">
          <Link to="/" className="font-semibold">DSA Queue</Link>
          <nav className="flex gap-3">
            {user?.isAdmin && (
              <Link to="/manage">
                <Button variant="ghost">Admin Panel</Button>
              </Link>
            )}
            {!user ? (
              <>
                <Link to="/login"><Button>Login</Button></Link>
                <Link to="/signup"><Button variant="outline">Signup</Button></Link>
              </>
            ) : (
              <Button variant="outline" onClick={logoutUser}>Logout</Button>
            )}
          </nav>
        </div>
      </header>
      <main className="flex-1 mx-auto max-w-5xl px-4 py-6">
        <Outlet />
      </main>
    </div>
  );
}
