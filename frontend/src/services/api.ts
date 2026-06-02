const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://localhost:8000";

export interface Source {
  video_id: string;
  platform: string;
  creator: string;
}

export interface ChatResponse {
  answer: string;
  sources: Source[];
}

/**
 * INGEST VIDEOS
 */
export async function ingestVideos(
  youtubeUrl: string,
  instagramUrl: string
) {
  const response = await fetch(`${API_BASE_URL}/ingest`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      youtube_url: youtubeUrl,
      instagram_url: instagramUrl,
    }),
  });

  if (!response.ok) {
    throw new Error("Video ingestion failed");
  }

  return response.json();
}

/**
 * CHAT WITH RAG
 */
export async function askQuestion(
  question: string,
  threadId: string = "default"
): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question,
      thread_id: threadId,
    }),
  });

  if (!response.ok) {
    throw new Error("Chat request failed");
  }

  return response.json();
}

/**
 * HEALTH CHECK
 */
export async function healthCheck() {
  const response = await fetch(`${API_BASE_URL}/health`);
  return response.json();
}