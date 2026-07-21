"use client";

import { useState } from "react";

interface Flashcard {
  term: string;
  definition: string;
}

function Card({ card }: { card: Flashcard }) {
  const [flipped, setFlipped] = useState(false);
  return (
    <div
      className={`flip-card h-40 cursor-pointer ${flipped ? "flipped" : ""}`}
      onClick={() => setFlipped((f) => !f)}
    >
      <div className="flip-card-inner w-full h-full">
        <div className="flip-card-front card w-full h-full p-4 flex items-center justify-center text-center">
          <p className="font-semibold text-brand-400">{card.term}</p>
        </div>
        <div className="flip-card-back card w-full h-full p-4 flex items-center justify-center text-center bg-brand-500/10">
          <p className="text-sm text-slate-200">{card.definition}</p>
        </div>
      </div>
    </div>
  );
}

export default function FlashcardGrid({ cards }: { cards: Flashcard[] }) {
  if (!cards?.length) return <p className="text-slate-500">No flashcards generated yet.</p>;
  return (
    <div className="grid sm:grid-cols-2 gap-4">
      {cards.map((c, i) => <Card key={i} card={c} />)}
    </div>
  );
}