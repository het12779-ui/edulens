"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import { askChat } from "@/lib/api";

interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: { content_id: string; excerpt: string; timestamp_seconds?: number | null; page_number?: number | null }[];
}

export default function ChatBox({
  contentId,
  onJumpToSource,
}: {
  contentId: string;
  onJumpToSource?: (ref: number) => void;
}) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const send = async () => {
    if (!input.trim()) return;
    const question = input.trim();
    setMessages((m) => [...m, { role: "user", content: question }]);
    setInput("");
    setLoading(true);
    try {
      const res = await askChat(contentId, question);
      setMessages((m) => [...m, { role: "assistant", content: res.answer, sources: res.sources }]);
    } catch {
      setMessages((m) => [...m, { role: "assistant", content: "Sorry, something went wrong answering that." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card flex flex-col h-[500px]">
      <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-4">
        {messages.length === 0 && (
          <p className="text-slate-500 text-sm">
            Ask anything about this document — e.g. "How does the author explain X?"
          </p>
        )}
        {messages.map((m, i) => (
          <div key={i} className={m.role === "user" ? "self-end max-w-[85%]" : "self-start max-w-[90%]"}>
            <div className={`rounded-lg px-3 py-2 text-sm ${m.role === "user" ? "bg-brand-500 text-white" : "bg-white/5 text-slate-200"}`}>
              <ReactMarkdown>{m.content}</ReactMarkdown>
            </div>
            {m.sources && m.sources.length > 0 && (
              <div className="flex flex-wrap gap-1 mt-1">
                {m.sources.map((s, j) => (
                  <button
                    key={j}
                    onClick={() => {
                      const ref = s.timestamp_seconds ?? s.page_number;
                      if (ref != null) onJumpToSource?.(ref);
                    }}
                    className="text-[11px] px-2 py-0.5 rounded-full bg-brand-500/10 text-brand-400 hover:bg-brand-500/20"
                    title={s.excerpt}
                  >
                    source {s.timestamp_seconds != null ? formatTime(s.timestamp_seconds) : `p.${s.page_number}`}
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}
        {loading && <p className="text-slate-500 text-sm animate-pulse">Thinking…</p>}
      </div>
      <div className="border-t border-white/5 p-3 flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          placeholder="Ask a question…"
          className="flex-1 bg-ink-900 border border-white/10 rounded-lg px-3 py-2 text-sm outline-none focus:border-brand-500"
        />
        <button onClick={send} disabled={loading} className="btn-primary">Send</button>
      </div>
    </div>
  );
}

function formatTime(seconds: number) {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}