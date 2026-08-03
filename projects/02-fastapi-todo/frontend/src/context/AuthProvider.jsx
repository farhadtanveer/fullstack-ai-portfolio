/* eslint-disable react-refresh/only-export-components */
import React from "react";
import { createContext, useState, useEffect } from "react";
import API from "../api/api";

export const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const login = async (credentials) => {
    const response = await API.post(
      "/token/",
      new URLSearchParams(credentials),
    );
    const { access_token } = response.data;
    localStorage.setItem("token", access_token);

    await getUser();
  };

  const signup = async (credentials) => {
    await API.post("/user/new_user/", credentials);
  };

  const getUser = async () => {
    try {
      const response = await API.get("/user/me/");
      setUser(response.data);
    } catch (error) {
      console.log(error);
      setUser(null);
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  useEffect(() => {
    getUser().finally(() => setLoading(false));
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, signup, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
