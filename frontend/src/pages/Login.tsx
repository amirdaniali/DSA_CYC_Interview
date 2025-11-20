// src/pages/Login.tsx
import { useState } from "react";
import { login } from "@/lib/auth";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useNavigate } from "react-router";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const nav = useNavigate();

  const submit = async () => {
    try {
      await login(username, password);
      nav("/admin/sessions");
    } catch {
      alert("Login failed");
    }
  };

  return (
    <Card className="max-w-md mx-auto p-6 space-y-4">
      <div className="space-y-2">
        <Label>Username</Label>
        <Input value={username} onChange={e=> setUsername(e.target.value)} />
      </div>
      <div className="space-y-2">
        <Label>Password</Label>
        <Input type="password" value={password} onChange={e=> setPassword(e.target.value)} />
      </div>
      <Button className="w-full" onClick={submit}>Sign in</Button>
    </Card>
  );
}
