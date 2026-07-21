"use client";
import FlashcardGrid from "@/components/FlashcardGrid";

export default function TestFlashcardsPage() {
  const fakeCards = [
    { term: "Recursion", definition: "A function that calls itself to solve smaller instances of the same problem." },
    { term: "Big-O Notation", definition: "A way to describe how an algorithm's runtime grows relative to input size." },
    { term: "Hash Table", definition: "A data structure that maps keys to values using a hash function for fast lookup." },
    { term: "Polymorphism", definition: "The ability of different object types to be accessed through the same interface." },
  ];

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-xl font-semibold mb-4">Flashcard test</h1>
      <FlashcardGrid cards={fakeCards} />
    </div>
  );
}