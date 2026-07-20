import axios from "axios";

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
});

export type ContentStatus = "queued" | "processing" | "ready" | "failed";

export interface ContentRecord {
  id: string;
  filename: string;
  source_type: "pdf" | "video" | "youtube";
  status: ContentStatus;
  transcript_preview?: string;
}

export async function uploadFile(file: File) {
  const form = new FormData();
  form.append("file", file);
  const { data } = await api.post("/api/upload/file", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

export async function uploadYoutube(url: string) {
  const form = new FormData();
  form.append("url", url);
  const { data } = await api.post("/api/upload/youtube", form);
  return data;
}

export async function askChat(contentId: string, question: string) {
  const { data } = await api.post("/api/chat", {
    content_id: contentId,
    question,
  });
  return data;
}