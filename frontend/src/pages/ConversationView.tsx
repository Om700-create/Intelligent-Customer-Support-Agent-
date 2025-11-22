import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Navbar from "../components/Navbar";
import { api } from "../api/client";
import MessageThread from "../components/MessageThread";

interface ConversationSummary {
  id: string;
  customer_id?: string;
  channel: string;
  status: string;
  last_intent?: string;
  last_sentiment?: string;
  last_confidence?: string;
  tags?: string;
  created_at: string;
  updated_at: string;
  assigned_agent_id?: string;
}

interface Message {
  id: string;
  sender_type: "customer" | "agent" | "ai" | "system";
  content: string;
  created_at: string;
}

interface Detail {
  conversation: ConversationSummary;
  messages: Message[];
}

const ConversationView: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [detail, setDetail] = useState<Detail | null>(null);
  const [loading, setLoading] = useState(true);

  const loadDetail = async () => {
    if (!id) return;
    setLoading(true);
    try {
      const resp = await api.get(`/admin/conversations/${id}`);
      setDetail(resp.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadDetail();
  }, [id]);

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="flex-1 bg-slate-100 p-6 flex gap-4">
        <div className="w-2/3">
          {loading || !detail ? (
            <div className="text-sm text-slate-500">Loading conversation...</div>
          ) : (
            <MessageThread messages={detail.messages} />
          )}
        </div>
        <div className="w-1/3">
          {!detail ? (
            <div className="text-sm text-slate-500">No details</div>
          ) : (
            <div className="border rounded-lg bg-white shadow-sm p-4 text-sm space-y-2">
              <h3 className="font-semibold text-slate-800 mb-2">Metadata</h3>
              <p>
                <span className="font-medium text-slate-700">Customer: </span>
                {detail.conversation.customer_id || "Anonymous"}
              </p>
              <p>
                <span className="font-medium text-slate-700">Status: </span>
                {detail.conversation.status}
              </p>
              <p>
                <span className="font-medium text-slate-700">Intent: </span>
                {detail.conversation.last_intent || "N/A"}
              </p>
              <p>
                <span className="font-medium text-slate-700">Sentiment: </span>
                {detail.conversation.last_sentiment || "N/A"}
              </p>
              <p>
                <span className="font-medium text-slate-700">Confidence: </span>
                {detail.conversation.last_confidence || "N/A"}
              </p>
              <p>
                <span className="font-medium text-slate-700">Tags: </span>
                {detail.conversation.tags || "None"}
              </p>
              <p className="text-xs text-slate-400">
                Created: {new Date(detail.conversation.created_at).toLocaleString()}
              </p>
              <p className="text-xs text-slate-400">
                Updated: {new Date(detail.conversation.updated_at).toLocaleString()}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ConversationView;
