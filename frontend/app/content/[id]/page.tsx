"use client";

import { useEffect, useRef, useState } from "react";
import { useParams } from "next/navigation";
import { getContent, ContentRecord, api } from "@/lib/api";
import InteractiveTimeline from "@/components/InteractiveTimeline";
import FlashcardGrid from "@/components/FlashcardGrid";
import ChatBox from "@/components/ChatBox";

type Tab = "outline" | "flashcards" | "chat";

export default function ContentDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [content, setContent] = useState<ContentRecord | null>(null);
  const [tab, setTab] = useState<Tab>("outline");
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const interval = setInterval(() => {
      getContent(id).then((c) => {
        setContent(c);
        if (c.status === "ready" || c.status === "failed") clearInterval(interval);
      });
    }, 3000);
    getContent(id).then(setContent);
    return () => clearInterval(interval);
  }, [id]);

  const isVideo = content?.source_type !== "pdf";

  const jumpTo = (ref: number) => {
    if (isVideo && videoRef.current) {
      videoRef.current.currentTime = ref;
      videoRef.current.play();
    } else {
      window.alert(`Jump to page ${ref} (PDF viewer wiring is a nice-to-have upgrade)`);
    }
  };

  if (!content) return <p className="text-slate-500">Loading…</p>;

  if (content.status !== "ready") {
    return (
      <div className="card p-10 text-center">
        <p className="text-lg font-medium">Processing your content…</p>
        <p className="text-slate-500 text-sm mt-1">Status: {content.status}. This page auto-refreshes.</p>
      </div>
    );
  }

  return (
    <div className="grid lg:grid-cols-[1fr_320px] gap-6">
      <div className="flex flex-col gap-6">
        <div className="card p-4">
          {isVideo ? (
            <video ref={videoRef} controls className="w-full rounded-lg" src={`${api.defaults.baseURL}/api/media/${content.id}`} />
          ) : (
            <div className="text-slate-400 text-sm p-4">
              PDF viewer placeholder — a real embedded viewer (e.g. react-pdf) is a nice future upgrade.
            </div>
          )}
        </div>

        <div className="flex gap-1 border-b border-white/5">
          {(["outline", "flashcards", "chat"] as Tab[]).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-4 py-2 text-sm capitalize border-b-2 transition-colors ${
                tab === t ? "border-brand-500 text-white" : "border-transparent text-slate-500 hover:text-slate-300"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        <div>
          {tab === "outline" && (
            <InteractiveTimeline outline={content.outline || []} isVideo={isVideo} onJump={jumpTo} />
          )}
          {tab === "flashcards" && <FlashcardGrid cards={content.flashcards || []} />}
          {tab === "chat" && <ChatBox contentId={content.id} onJumpToSource={jumpTo} />}
        </div>
      </div>

      <aside className="card p-4 h-fit">
        <p className="text-slate-500 text-xs uppercase tracking-wide mb-2">Now viewing</p>
        <p className="font-medium truncate">{content.filename}</p>
        <p className="text-slate-500 text-sm mt-3 line-clamp-6">{content.transcript_preview}</p>
      </aside>
    </div>
  );
}