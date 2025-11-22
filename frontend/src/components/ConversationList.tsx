import React from "react";
import { Link } from "react-router-dom";

interface Conversation {
  id: string;
  customer_id?: string;
  status: string;
  last_intent?: string;
  last_sentiment?: string;
  tags?: string;
  created_at: string;
}

interface Props {
  items: Conversation[];
}

const ConversationList: React.FC<Props> = ({ items }) => {
  return (
    <div className="border rounded-lg bg-white shadow-sm overflow-hidden">
      <div className="px-4 py-2 border-b text-sm font-semibold text-slate-700 bg-slate-50">
        Conversations
      </div>
      <div className="divide-y">
        {items.length === 0 && (
          <div className="px-4 py-4 text-sm text-slate-500">No conversations yet.</div>
        )}
        {items.map((c) => (
          <Link
            key={c.id}
            to={`/conversations/${c.id}`}
            className="flex flex-col gap-1 px-4 py-2 hover:bg-slate-50 text-sm"
          >
            <div className="flex justify-between items-center">
              <span className="font-semibold text-slate-800">
                {c.customer_id || "Anonymous"}
              </span>
              <span className="text-xs rounded-full px-2 py-0.5 bg-slate-100 text-slate-600 capitalize">
                {c.status}
              </span>
            </div>
            <div className="flex flex-wrap gap-1 text-xs text-slate-500">
              {c.last_intent && <span>Intent: {c.last_intent}</span>}
              {c.last_sentiment && <span>Sentiment: {c.last_sentiment}</span>}
            </div>
            <div className="text-xs text-slate-400">
              {new Date(c.created_at).toLocaleString()}
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default ConversationList;
