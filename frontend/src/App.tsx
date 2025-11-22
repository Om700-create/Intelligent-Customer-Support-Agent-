import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import ChatCustomer from "./pages/ChatCustomer";
import Dashboard from "./pages/Dashboard";
import ConversationView from "./pages/ConversationView";
import { useAuthState } from "./store/authStore";

const App: React.FC = () => {
  const { token } = useAuthState();

  return (
    <Routes>
      <Route path="/" element={<ChatCustomer />} />
      <Route path="/login" element={<Login />} />
      <Route
        path="/dashboard"
        element={token ? <Dashboard /> : <Navigate to="/login" replace />}
      />
      <Route
        path="/conversations/:id"
        element={token ? <ConversationView /> : <Navigate to="/login" replace />}
      />
    </Routes>
  );
};

export default App;
