"use client";
import ChatBox from "@/components/ChatBox";

export default function TestChatPage() {
  // Replace with a real content_id that has indexed chunks (from your Hour 14 test_check_index.py output)
  const CONTENT_ID = "test-content-123";

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-xl font-semibold mb-4">Chat test — content_id: {CONTENT_ID}</h1>
      <ChatBox contentId={CONTENT_ID} />
    </div>
  );
}