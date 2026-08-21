import { Navigate } from "react-router-dom";

import { useAuth } from "./AuthContext.jsx";

export function ProtectedRoute({ children }) {
  const { username } = useAuth();

  if (username === undefined) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-bg">
        <p className="font-display text-[12px] text-text-dim">CHECKING SESSION…</p>
      </div>
    );
  }

  if (username === null) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
