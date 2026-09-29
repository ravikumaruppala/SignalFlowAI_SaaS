import { createContext, useContext, useEffect, useState } from "react";
import api, { initCsrf, apiError } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    (async () => {
      try {
        await initCsrf();
        const r = await api.get("/auth/me/");
        setUser(r.data.user);
      } catch {
        setUser(null);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  async function login(email, password, rememberMe = false) {
    setError("");
    await initCsrf();
    try {
      const r = await api.post("/auth/login/", {
        email,
        password,
        remember_me: rememberMe,
      });
      setUser(r.data.user);
      await initCsrf();
      return true;
    } catch (e) {
      setError(apiError(e));
      return false;
    }
  }

  async function register(payload) {
    setError("");
    await initCsrf();
    try {
      const r = await api.post("/auth/register/", payload);
      setUser(r.data.user);
      await initCsrf();
      return true;
    } catch (e) {
      setError(apiError(e));
      return false;
    }
  }

  async function logout() {
    try {
      await api.post("/auth/logout/");
    } finally {
      setUser(null);
    }
  }

  async function refreshUser() {
    const r = await api.get("/auth/me/");
    setUser(r.data.user);
  }

  return (
    <AuthContext.Provider
      value={{ user, loading, error, login, register, logout, refreshUser }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
