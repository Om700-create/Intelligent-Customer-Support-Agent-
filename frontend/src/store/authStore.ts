import { useState } from "react";
import { setAuthToken } from "../api/client";

export function useAuthState() {
  const [token, setToken] = useState<string | null>(localStorage.getItem("access_token"));
  const [userEmail, setUserEmail] = useState<string | null>(localStorage.getItem("user_email"));

  const login = (accessToken: string, email: string) => {
    setToken(accessToken);
    setAuthToken(accessToken);
    setUserEmail(email);
    localStorage.setItem("access_token", accessToken);
    localStorage.setItem("user_email", email);
  };

  const logout = () => {
    setToken(null);
    setUserEmail(null);
    setAuthToken(null);
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_email");
  };

  if (token) {
    setAuthToken(token);
  }

  return { token, userEmail, login, logout };
}
