import { createContext, useContext, useEffect, useState } from "react";

import {
  login as apiLogin,
  logout as apiLogout,
  me as apiMe,
  register as apiRegister,
} from "../api/client.js";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [email, setEmail] = useState(undefined); // undefined = loading, null = signed out

  useEffect(() => {
    apiMe().then((result) => setEmail(result ? result.email : null));
  }, []);

  async function signIn(userEmail, password) {
    const result = await apiLogin(userEmail, password);
    setEmail(result.email);
  }

  async function signUp(userEmail, password) {
    const result = await apiRegister(userEmail, password);
    setEmail(result.email);
  }

  async function signOut() {
    await apiLogout();
    setEmail(null);
  }

  return (
    <AuthContext.Provider value={{ email, signIn, signUp, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
