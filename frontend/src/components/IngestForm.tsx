"use client";

import { useState } from "react";
import { ingestVideos } from "../services/api";
import VideoCard from "./VideoCard";
import { VideoMetadata } from "../types";

export default function IngestForm() {
  const [youtubeUrl, setYoutubeUrl] = useState<string>("");
  const [instagramUrl, setInstagramUrl] = useState<string>("");

  const [videoA, setVideoA] = useState<VideoMetadata | null>(null);
  const [videoB, setVideoB] = useState<VideoMetadata | null>(null);

  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  async function handleIngest() {
    const yt = youtubeUrl.trim();
    const ig = instagramUrl.trim();

    if (!yt || !ig) {
      setError("Both YouTube and Instagram URLs are required.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const data = await ingestVideos(yt, ig);

      setVideoA(data?.video_a ?? null);
      setVideoB(data?.video_b ?? null);
    } catch (err) {
      console.error("Ingest error:", err);
      setError("Failed to ingest videos. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="border rounded-lg p-5 bg-white shadow-sm">
      <h2 className="text-xl font-semibold mb-4">
        Video Ingestion
      </h2>

      {/* INPUTS */}
      <input
        placeholder="YouTube URL"
        value={youtubeUrl}
        onChange={(e) => setYoutubeUrl(e.target.value)}
        className="border p-2 w-full rounded"
      />

      <input
        placeholder="Instagram URL"
        value={instagramUrl}
        onChange={(e) => setInstagramUrl(e.target.value)}
        className="border p-2 w-full mt-2 rounded"
      />

      {/* ERROR */}
      {error && (
        <p className="text-red-500 text-sm mt-2">
          {error}
        </p>
      )}

      {/* BUTTON */}
      <button
        onClick={handleIngest}
        disabled={loading}
        className={`mt-3 px-4 py-2 border rounded transition ${
          loading
            ? "opacity-60 cursor-not-allowed"
            : "hover:bg-gray-100"
        }`}
      >
        {loading ? "Analyzing..." : "Analyze Videos"}
      </button>

      {/* RESULTS */}
      {(videoA || videoB) && (
        <div className="grid grid-cols-2 gap-4 mt-6">
          {videoA && <VideoCard video={videoA} />}
          {videoB && <VideoCard video={videoB} />}
        </div>
      )}
    </div>
  );
}