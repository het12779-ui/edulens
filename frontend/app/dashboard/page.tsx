"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getLibrary, ContentRecord } from "@/lib/api";

const statusColor: Record<string, string> = {
  queued: "bg-slate-500/20 text-slate-300",
  processing: "bg-amber-500/20 text-amber-300",
  ready: "bg-emerald-500/20 text-emerald-300",
  failed: "bg-red-500/20 text-red-300",
};

export default function DashboardPage() {
  const [items, setItems] = useState<ContentRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = () => getLibrary().then(setItems).finally(() => setLoading(false));
    load();
    const interval = setInterval(load, 4000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-semibold">Your Library</h1>
        <Link href="/upload" className="btn-primary">+ New upload</Link>
      </div>

      {loading && <p className="text-slate-500">Loading…</p>}
      {!loading && items.length === 0 && (
        <div className="card p-10 text-center text-slate-400">
          Nothing here yet. <Link href="/upload" className="text-brand-400">Upload your first file</Link>.
        </div>
      )}

      <div className="grid md:grid-cols-3 gap-4">
        {items.map((item) => (
          <Link
            key={item.id}
            href={`/content/${item.id}`}
            className="card p-5 border hover:border-brand-500/50 transition-colors"
          >
            <div className="flex items-center justify-between mb-3">
              <span className="badge bg-white/5 text-slate-300 uppercase">{item.source_type}</span>
              <span className={`badge ${statusColor[item.status]}`}>{item.status}</span>
            </div>
            <p className="font-medium truncate">{item.filename}</p>
            {item.transcript_preview && (
              <p className="text-slate-500 text-sm mt-2 line-clamp-2">{item.transcript_preview}</p>
            )}
          </Link>
        ))}
      </div>
    </div>
  );
}