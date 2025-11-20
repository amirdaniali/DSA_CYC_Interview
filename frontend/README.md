# DSA Interview Queue – React MVP

A minimal scheduling app for managing DSA interview practice sessions.  
Students can view sessions and sign up for the queue. Admins can create, update, and close sessions.

---

## Technology Choices

- **React + TypeScript** – Strong typing and modern component architecture.
- **Vite** – Fast dev server and build tool.
- **React Router** – Client-side routing for pages (`/sessions`, `/admin/sessions`, `/login`).
- **shadcn/ui + TailwindCSS** – Prebuilt accessible UI components with Tailwind styling.
- **Axios** – HTTP client for communicating with the backend API.
- **Sonner** – Toast notifications for success/error feedback.
- **JWT Auth** – Authentication with access/refresh tokens from the backend.

---

## Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/your-org/dsa-queue.git
cd dsa-queue
npm install
```

## Authentication

- Tokens are stored in localStorage (access, refresh).
- Login via /api/token/ with username/password.
- Axios interceptors automatically attach the Authorization: Bearer <token> header and refresh expired tokens.

## Main Code Paths

`src/lib/api.ts`

- Configures Axios instance.
- Handles token injection and refresh logic.

`src/lib/types.ts`
- TypeScript interfaces for Session, Signup, and TokenPair.

`src/lib/sessionApi.ts` / `src/lib/signupApi.ts`

- CRUD functions for sessions and signups.

- Example: listSessions(), createSignup(payload).

`src/lib/auth.ts`

- login(username, password) → stores tokens in localStorage.



## UI Components

- Card, Button, Input, Select, Label – from shadcn/ui.
- Sonner Toaster – global toast provider in main.tsx.
- Responsive layout – Tailwind grid and spacing utilities.

## Usage Flow

-Student opens / → sees sessions → selects LC level → clicks Join queue.
-Admin logs in → goes to /admin/sessions → creates sessions → closes them when appointments are set.
-Logout button clears tokens and returns to login.

## Future Improvements

- Better signup management (view your own signup).
- Session capacity enforcement.
- Deployment pipeline 
- Docker
- Better UI
