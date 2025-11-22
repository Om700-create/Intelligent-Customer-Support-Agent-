import React from "react";

interface Message {
  id: string;
  sender_type: "customer" | "agent" | "ai" | "system";
  content: string;
  created_at: string;
}

interface Props {
  messages: Message[];
}

const MessageThread: React.FC<Props> = ({ messages }) => {
  const getLabelColor = (sender: Message["sender_type"]) => {
    switch (sender) {
      case "customer":
        return "bg-blue-50 text-blue-700";
      case "agent":
        return "bg-emerald-50 text-emerald-700";
      case "ai":
        return "bg-slate-100 text-slate-700";
      case "system":
        return "bg-orange-50 text-orange-700";
    }
  };

  return (
    <div className="border rounded-lg bg-white shadow-sm h-full flex flex-col">
      <div className="px-4 py-2 border-b text-sm font-semibold text-slate-700 bg-slate-50">
        Messages
      </div>
      <div className="flex-1 overflow-y-auto px-4 py-3 space-y-3">
        {messages.length === 0 && (
          <div className="text-sm text-slate-500">No messages in this conversation.</div>
        )}
        {messages.map((m) => (
          <div key={m.id} className="flex flex-col gap-1 text-sm">
            <div className={`inline-block px-2 py-0.5 rounded-full text-xs ${getLabelColor(m.sender_type)}`}>
              {m.sender_type.toUpperCase()}
            </div>
            <div className="bg-slate-50 border border-slate-100 rounded-md px-3 py-2 whitespace-pre-wrap">
              {m.content}
            </div>
            <div className="text-xs text-slate-400">
              {new Date(m.created_at).toLocaleString()}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MessageThread;
