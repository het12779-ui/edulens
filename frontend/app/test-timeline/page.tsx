"use client";
import InteractiveTimeline from "@/components/InteractiveTimeline";

export default function TestTimelinePage() {
  const fakeOutline = [
    { title: "Introduction", summary: "Overview of the topic and why it matters.", timestamp_seconds: 0 },
    { title: "Core Concept", summary: "The main idea explained with an example.", timestamp_seconds: 125 },
    { title: "Deeper Dive", summary: "Edge cases and common misconceptions.", timestamp_seconds: 340 },
  ];

  return (
    <div className="max-w-xl mx-auto">
      <h1 className="text-xl font-semibold mb-4">Timeline test</h1>
      <InteractiveTimeline
        outline={fakeOutline}
        isVideo={true}
        onJump={(ref) => alert(`Would jump to ${ref} seconds`)}
      />
    </div>
  );
}