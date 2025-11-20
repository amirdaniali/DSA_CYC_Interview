import { StrictMode } from 'react'
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router";
import AppLayout from "./ui/AppLayout";
import Home from "./pages/Home";
import Sessions from "./pages/Sessions";
import AdminSessions from "./pages/admin/AdminSessions";
import Login from "./pages/Login";
import { Toaster } from "sonner";

import "./index.css";


createRoot(document.getElementById("root")!).render(
  <StrictMode>
  <BrowserRouter>
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<Home />} />
        <Route path="/sessions" element={<Sessions />} />
        <Route path="/admin/sessions" element={<AdminSessions />} />
        <Route path="/login" element={<Login />} />
      </Route>
    </Routes>
    <Toaster richColors />   {/* global toast provider */}
  </BrowserRouter>
  </StrictMode>,
);
