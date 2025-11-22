import React, { useEffect, useState } from "react";
import { api } from "../api/client";
import Navbar from "../components/Navbar";
import ConversationList from "../components/ConversationList";

interface Conversation {
  id: string;
  customer_id?: string;
  status: string;
  last_intent?: string;
  last_sentiment?: string;
  tags?: string;
  created_at: string;
  updated_at: string;
}

const Dashboard: React.FC = () => {
  const [convos, setConvos] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);

  const loadConvos = async () => {
    setLoading(true);
    try {
      const resp = await api.get("/admin/conversations");
      setConvos(resp.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadConvos();
  }, []);

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="flex-1 bg-slate-100 p-6">
        <h2 className="text-xl font-semibold text-slate-800 mb-4">
          Conversation Dashboard
        </h2>
        {loading ? (
          <div className="text-sm text-slate-500">Loading conversations...</div>
        ) : (
          <ConversationList items={convos} />
        )}
      </div>
    </div>
  );
};

export default Dashboard;
