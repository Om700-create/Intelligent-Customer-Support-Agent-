import React, { useState } from "react";
import { api } from "../api/client";

interface Message {
  from: "user" | "ai";
  content: string;
}

const ChatCustomer: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [customerId] = useState(
    () => localStorage.getItem("customer_id") || `cust-${crypto.randomUUID()}`
  );
  const [loading, setLoading] = useState(false);

  React.useEffect(() => {
    localStorage.setItem("customer_id", customerId);
  }, [customerId]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg: Message = { from: "user", content: input.trim() };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const resp = await api.post("/chat/message", {
        customer_id: customerId,
        message: input.trim(),
        channel: "web"
      });
      const reply = resp.data.reply as string;
      const aiMsg: Message = { from: "ai", content: reply };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      console.error(err);
    } finally {
      setInput("");
      setLoading(false);
    }
  };

  const handleKeyDown: React.KeyboardEventHandler<HTMLTextAreaElement> = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      void sendMessage();
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center bg-gradient-to-br from-slate-100 to-slate-200">
      <div className="w-full max-w-3xl mt-10 bg-white shadow-lg rounded-xl flex flex-col h-[70vh]">
        <div className="px-6 py-4 border-b border-slate-200">
          <h1 className="text-xl font-bold text-slate-800">
            Intelligent Customer Support
          </h1>
          <p className="text-sm text-slate-500">
            Describe your issue. Our AI agent will help you.
          </p>
        </div>
        <div className="flex-1 overflow-y-auto px-4 py-3 space-y-2">
          {messages.length === 0 && (
            <div className="text-center text-slate-500 mt-10 text-sm">
              Start by typing your question below.
            </div>
          )}
          {messages.map((m, idx) => (
            <div
              key={idx}
              className={`flex ${
                m.from === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`px-3 py-2 rounded-lg max-w-[75%] text-sm ${
                  m.from === "user"
                    ? "bg-blue-600 text-white rounded-br-sm"
                    : "bg-slate-100 text-slate-800 rounded-bl-sm"
                }`}
              >
                {m.content}
              </div>
            </div>
          ))}
          {loading && (
            <div className="text-sm text-slate-500 animate-pulse">
              Support agent is typing...
            </div>
          )}
        </div>
        <div className="border-t border-slate-200 p-3 flex gap-2">
          <textarea
            className="flex-1 border rounded-md px-3 py-2 text-sm focus:outline-none focus:ring focus:ring-blue-200 resize-none"
            rows={2}
            placeholder="Describe your issue..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <button
            onClick={sendMessage}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 text-white rounded-md px-4 py-2 text-sm font-semibold disabled:opacity-60"
          >
            Send
          </button>
        </div>
      </div>
      <a
        href="/login"
        className="mt-4 text-xs text-slate-500 hover:text-slate-700"
      >
        Agent / Admin login
      </a>
    </div>
  );
};

export default ChatCustomer;
