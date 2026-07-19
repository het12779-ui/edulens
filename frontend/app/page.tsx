export default function HomePage() {
    return (
      <div className="flex flex-col items-center text-center gap-6 py-16">
        <span className="badge bg-brand-500/10 text-brand-400 border border-brand-500/30">
          AI-Powered Study Companion
        </span>
        <h1 className="text-4xl md:text-5xl font-bold max-w-2xl leading-tight">
          Turn 1-hour lectures and 50-page PDFs into a{" "}
          <span className="text-brand-400">10-minute interactive study guide</span>
        </h1>
        <p className="text-slate-400 max-w-xl">
          Drop in a video, YouTube link, or PDF. EduLens builds a clickable chapter outline,
          auto-generated flashcards, a knowledge graph, and a chat box that answers
          questions straight from your material.
        </p>
      </div>
    );
  }