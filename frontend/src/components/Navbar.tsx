import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuthState } from "../store/authStore";

const Navbar: React.FC = () => {
  const { userEmail, logout } = useAuthState();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="w-full flex items-center justify-between px-6 py-3 border-b bg-white">
      <Link to="/dashboard" className="text-lg font-bold text-slate-800">
        Support Admin
      </Link>
      <div className="flex items-center gap-4 text-sm">
        {userEmail && <span className="text-slate-500">{userEmail}</span>}
        <button
          onClick={handleLogout}
          className="border border-slate-300 text-slate-700 px-3 py-1 rounded-md hover:bg-slate-50"
        >
          Logout
        </button>
      </div>
    </div>
  );
};

export default Navbar;
