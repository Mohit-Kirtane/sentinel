import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";

import { useAuth } from "../auth/AuthContext.jsx";

export default function LoginPage() {
  const { email, signIn, signUp } = useAuth();
  const navigate = useNavigate();
  const [mode, setMode] = useState("signin"); // "signin" | "signup"
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  if (email) return <Navigate to="/app" replace />;

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      if (mode === "signin") {
        await signIn(form.email, form.password);
      } else {
        await signUp(form.email, form.password);
      }
      navigate("/app");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-bg px-6">
      <div className="w-full max-w-sm rounded-lg border border-line bg-surface p-8">
        <div className="mb-6 flex items-center gap-2">
          <span className="rec-pulse h-2 w-2 rounded-full bg-rec" />
          <span className="font-display text-sm font-semibold tracking-[0.14em] text-text">
            SENTINEL
          </span>
        </div>
        <h2 className="font-body text-lg font-semibold text-text">
          {mode === "signin" ? "Sign in" : "Create an account"}
        </h2>
        <p className="mt-1 font-body text-sm text-text-dim">
          {mode === "signin"
            ? "Access the monitoring console."
            : "Get access to the monitoring console."}
        </p>

        <form onSubmit={handleSubmit} className="mt-6 space-y-3">
          <input
            type="email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            placeholder="Email"
            autoFocus
            className="w-full rounded-md border border-line bg-bg px-3 py-2 font-body text-sm text-text placeholder:text-text-dim focus:outline-none"
          />
          <input
            type="password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            placeholder="Password"
            className="w-full rounded-md border border-line bg-bg px-3 py-2 font-body text-sm text-text placeholder:text-text-dim focus:outline-none"
          />
          {error && <p className="font-body text-sm text-rec">{error}</p>}
          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-md bg-rec px-4 py-2 font-display text-[12px] font-medium tracking-wide text-white transition hover:bg-rec-deep disabled:opacity-40"
          >
            {loading ? "PLEASE WAIT…" : mode === "signin" ? "SIGN IN" : "CREATE ACCOUNT"}
          </button>
        </form>

        <button
          onClick={() => {
            setMode(mode === "signin" ? "signup" : "signin");
            setError(null);
          }}
          className="mt-4 w-full font-body text-sm text-text-dim transition hover:text-text"
        >
          {mode === "signin" ? "Need an account? Create one" : "Already have an account? Sign in"}
        </button>
      </div>
    </div>
  );
}
