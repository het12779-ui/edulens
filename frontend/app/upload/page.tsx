"use client";

import { useState, useCallback } from "react";
import { uploadFile, uploadYoutube } from "@/lib/api";

export default function UploadPage() {
  const [dragging, setDragging] = useState(false);
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleFile = useCallback(async (file: File) => {
    setBusy(true);
    try {
      const res = await uploadFile(file);
      setResult(res);
    } catch (e: any) {
      alert(e?.response?.data?.detail || "Upload failed");
    } finally {
      setBusy(false);
    }
  }, []);

  const handleYoutube = async () => {
    if (!youtubeUrl.trim()) return;
    setBusy(true);
    try {
      const res = await uploadYoutube(youtubeUrl.trim());
      setResult(res);
    } catch (e: any) {
      alert(e?.response?.data?.detail || "Could not process that link");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto flex flex-col gap-8">
      <div>
        <h1 className="text-2xl font-semibold">Upload study material</h1>
        <p className="text-slate-400 text-sm mt-1">PDF, MP4/MOV/MP3, or paste a YouTube link.</p>
      </div>

      <div
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragging(false);
          const file = e.dataTransfer.files?.[0];
          if (file) handleFile(file);
        }}
        className={`card p-10 text-center border-2 border-dashed transition-colors ${
          dragging ? "border-brand-500 bg-brand-500/5" : "border-white/10"
        }`}
      >
        <p className="text-slate-300 mb-3">Drag & drop a file here, or</p>
        <label className="btn-primary cursor-pointer inline-block">
          Browse files
          <input
            type="file"
            className="hidden"
            accept=".pdf,.mp4,.mov,.mkv,.mp3,.wav,.m4a"
            onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
          />
        </label>
        {busy && <p className="text-brand-400 text-sm mt-3">Uploading…</p>}
      </div>

      <div className="flex items-center gap-3 text-slate-500 text-sm">
        <div className="h-px bg-white/10 flex-1" /> OR <div className="h-px bg-white/10 flex-1" />
      </div>

      <div className="card p-6 flex gap-3">
        <input
          value={youtubeUrl}
          onChange={(e) => setYoutubeUrl(e.target.value)}
          placeholder="Paste a YouTube link…"
          className="flex-1 bg-ink-900 border border-white/10 rounded-lg px-3 py-2 text-sm outline-none focus:border-brand-500"
        />
        <button onClick={handleYoutube} disabled={busy} className="btn-primary">
          Process
        </button>
      </div>

      {result && (
        <pre className="card p-4 text-xs text-slate-400 overflow-auto">
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  );
}