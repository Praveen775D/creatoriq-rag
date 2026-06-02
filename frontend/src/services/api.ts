const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * INGEST VIDEOS (YouTube + Instagram)
 */
export async function ingestVideos(
  youtubeUrl: string,
  instagramUrl: string
) {
  const res = await fetch(`${API_BASE_URL}/ingest`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      youtube_url: youtubeUrl,
      instagram_url: instagramUrl
    })
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || "Ingestion failed");
  }

  return res.json();
}

/**
 * CHAT (RAG)
 */
export async function askQuestion(
  question: string,
  threadId: string = "default-thread"
): Promise<import("../types").ChatResponse> {
  const res = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      question,
      thread_id: threadId
    })
  });

  if (!res.ok) {
    throw new Error("Chat request failed");
  }

  return res.json();
}

/**
 * HEALTH CHECK
 */
export async function healthCheck() {
  const res = await fetch(`${API_BASE_URL}/health`);
  return res.json();
}