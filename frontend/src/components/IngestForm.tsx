"use client";

import { useState } from "react";
import { ingestVideos } from "../services/api";
import VideoCard from "./VideoCard";
import { VideoMetadata } from "../types";

export default function IngestForm() {
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [instagramUrl, setInstagramUrl] = useState("");

  const [videoA, setVideoA] = useState<VideoMetadata | null>(null);
  const [videoB, setVideoB] = useState<VideoMetadata | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleIngest() {
    const yt = youtubeUrl.trim();
    const ig = instagramUrl.trim();

    if (!yt || !ig) {
      setError("Please enter both YouTube and Instagram URLs.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const data = await ingestVideos(yt, ig);

      setVideoA(data?.video_a ?? null);
      setVideoB(data?.video_b ?? null);
    } catch (err) {
      console.error(err);
      setError("Failed to analyze videos. Try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto w-full max-w-3xl rounded-2xl border border-gray-100 bg-white p-6 shadow-sm">

      {/* HEADER */}
      <div className="mb-5">
        <h2 className="text-2xl font-bold text-gray-900">
          Video Intelligence Dashboard
        </h2>
        <p className="mt-1 text-sm text-gray-500">
          Compare YouTube and Instagram performance in seconds
        </p>
      </div>

      {/* INPUT SECTION */}
      <div className="space-y-3">
        <div>
          <label className="text-xs font-medium text-gray-600">
            YouTube URL
          </label>
          <input
            value={youtubeUrl}
            onChange={(e) => setYoutubeUrl(e.target.value)}
            placeholder="https://youtube.com/..."
            className="mt-1 w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm outline-none transition focus:border-black focus:bg-white"
          />
        </div>

        <div>
          <label className="text-xs font-medium text-gray-600">
            Instagram URL
          </label>
          <input
            value={instagramUrl}
            onChange={(e) => setInstagramUrl(e.target.value)}
            placeholder="https://instagram.com/..."
            className="mt-1 w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm outline-none transition focus:border-black focus:bg-white"
          />
        </div>
      </div>

      {/* ERROR */}
      {error && (
        <div className="mt-3 rounded-lg border border-red-100 bg-red-50 px-3 py-2 text-sm text-red-600">
          {error}
        </div>
      )}

      {/* BUTTON */}
      <button
        onClick={handleIngest}
        disabled={loading}
        className={`mt-5 w-full rounded-xl px-4 py-3 text-sm font-semibold text-white transition ${
          loading
            ? "cursor-not-allowed bg-gray-400"
            : "bg-gradient-to-r from-black to-gray-800 hover:opacity-90"
        }`}
      >
        {loading ? "Analyzing videos..." : "Analyze & Compare"}
      </button>

      {/* RESULTS */}
      {(videoA || videoB) && (
        <div className="mt-8">
          <h3 className="mb-3 text-sm font-semibold text-gray-700">
            Comparison Results
          </h3>

          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            {videoA && <VideoCard video={videoA} />}
            {videoB && <VideoCard video={videoB} />}
          </div>
        </div>
      )}
    </div>
  );
}