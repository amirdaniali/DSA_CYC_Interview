import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useNavigate } from "react-router";
import { signup } from "@/lib/auth";

export default function Signup() {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [fullName, setFullName] = useState("");
    const [discordUsername, setDiscordUsername] = useState("");
    const [password, setPassword] = useState("");
    const nav = useNavigate();

    const submit = async () => {
        try {
            const payload = {
                username,
                email,
                full_name: fullName,
                discord_username: discordUsername,
                password,
            };
            console.log("[Signup] Creating user:", payload);

            const data = await signup(payload);
            console.log("[Signup] User created successfully:", data);

            alert("Signup successful! Please log in.");
            nav("/login");
        } catch (err) {
            console.error("[Signup] Signup failed:", err);
            alert("Signup failed");
        }
    };

    return (
        <Card className="max-w-md mx-auto p-6 space-y-4">
            <div className="space-y-2">
                <Label>Username</Label>
                <Input value={username} onChange={(e) => setUsername(e.target.value)} />
            </div>
            <div className="space-y-2">
                <Label>Email</Label>
                <Input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
            </div>
            <div className="space-y-2">
                <Label>Full Name</Label>
                <Input value={fullName} onChange={(e) => setFullName(e.target.value)} />
            </div>
            <div className="space-y-2">
                <Label>Discord Username</Label>
                <Input value={discordUsername} onChange={(e) => setDiscordUsername(e.target.value)} />
            </div>
            <div className="space-y-2">
                <Label>Password</Label>
                <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
            </div>
            <Button className="w-full" onClick={submit}>Sign up</Button>
        </Card>
    );
}
