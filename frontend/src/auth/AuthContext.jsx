import { createContext, useContext, useEffect, useState } from "react";

import { login as apiLogin, logout as apiLogout, me as apiMe } from "../api/client.js";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [username, setUsername] = useState(undefined); // undefined = loading, null = signed out

  useEffect(() => {
    apiMe().then((result) => setUsername(result ? result.username : null));
  }, []);

  async function signIn(user, password) {
    const result = await apiLogin(user, password);
    setUsername(result.username);
  }

  async function signOut() {
    await apiLogout();
    setUsername(null);
  }

  return (
    <AuthContext.Provider value={{ username, signIn, signOut }}>{children}</AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
