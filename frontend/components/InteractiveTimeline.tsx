"use client";

interface OutlineItem {
  title: string;
  summary: string;
  timestamp_seconds?: number | null;
  page_number?: number | null;
}

export default function InteractiveTimeline({
  outline,
  isVideo,
  onJump,
}: {
  outline: OutlineItem[];
  isVideo: boolean;
  onJump: (ref: number) => void;
}) {
  if (!outline?.length) return <p className="text-slate-500">Outline is still being generated…</p>;

  return (
    <ol className="flex flex-col gap-1">
      {outline.map((item, i) => {
        const ref = isVideo ? item.timestamp_seconds : item.page_number;
        return (
          <li key={i}>
            <button
              onClick={() => ref != null && onJump(ref)}
              className="w-full text-left px-3 py-3 rounded-lg hover:bg-white/5 transition-colors flex gap-3 group"
            >
              <span className="text-brand-400 text-xs font-mono mt-0.5 shrink-0 w-14">
                {isVideo ? formatTime(item.timestamp_seconds) : `p. ${item.page_number}`}
              </span>
              <span>
                <span className="font-medium group-hover:text-brand-400 transition-colors">{item.title}</span>
                <p className="text-slate-500 text-sm mt-0.5">{item.summary}</p>
              </span>
            </button>
          </li>
        );
      })}
    </ol>
  );
}

function formatTime(seconds?: number | null) {
  if (seconds == null) return "--:--";
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}