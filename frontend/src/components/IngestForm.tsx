"use client";

import { useState } from "react";
import { ingestVideos } from "../services/api";
import VideoCard from "./VideoCard";
import { VideoMetadata } from "../types";

export default function IngestForm() {
const [youtubeUrl, setYoutubeUrl] = useState("");
const [instagramUrl, setInstagramUrl] = useState("");

const [videoA, setVideoA] =
useState<VideoMetadata | null>(null);

const [videoB, setVideoB] =
useState<VideoMetadata | null>(null);

const [loading, setLoading] = useState(false);
const [error, setError] = useState("");

async function handleIngest() {
if (!youtubeUrl.trim() || !instagramUrl.trim()) {
setError("Both URLs are required");
return;
}


try {
  setLoading(true);
  setError("");

  const data = await ingestVideos(
    youtubeUrl,
    instagramUrl
  );

  setVideoA(data?.video_a || null);
  setVideoB(data?.video_b || null);
} catch (err) {
  console.error(err);
  setError("Failed to analyze videos");
} finally {
  setLoading(false);
}


}

return ( <div className="space-y-12">


  {/* INPUT SECTION */}
  <div className="grid lg:grid-cols-[1fr_auto_1fr] gap-8 items-center">

    {/* YOUTUBE */}
    <div
      className="
      rounded-[32px]
      border
      border-red-500/20
      bg-gradient-to-br
      from-red-500/5
      to-transparent
      p-8
      "
    >
      <div className="flex items-center gap-4 mb-6">

        <div className="h-14 w-14 rounded-2xl bg-red-500 flex items-center justify-center text-2xl">
          ▶
        </div>

        <div>
          <h3 className="text-xl font-bold">
            YouTube Short
          </h3>

          <p className="text-slate-400 text-sm">
            Video A
          </p>
        </div>

      </div>

      <input
        value={youtubeUrl}
        onChange={(e) =>
          setYoutubeUrl(e.target.value)
        }
        placeholder="Paste YouTube Shorts URL"
        className="
          w-full
          h-14
          rounded-2xl
          bg-[#111827]
          border
          border-white/10
          px-5
          outline-none
          focus:border-red-500
        "
      />
    </div>

    {/* VS */}
    <div
      className="
      h-24
      w-24
      rounded-full
      border
      border-white/10
      bg-white/[0.03]
      flex
      items-center
      justify-center
      font-black
      text-xl
      "
    >
      VS
    </div>

    {/* INSTAGRAM */}
    <div
      className="
      rounded-[32px]
      border
      border-pink-500/20
      bg-gradient-to-br
      from-pink-500/5
      to-transparent
      p-8
      "
    >
      <div className="flex items-center gap-4 mb-6">

        <div className="h-14 w-14 rounded-2xl bg-gradient-to-r from-pink-500 to-violet-500 flex items-center justify-center text-2xl">
          
        </div>

        <div>
          <h3 className="text-xl font-bold">
            Instagram Reel
          </h3>

          <p className="text-slate-400 text-sm">
            Video B
          </p>
        </div>

      </div>

      <input
        value={instagramUrl}
        onChange={(e) =>
          setInstagramUrl(e.target.value)
        }
        placeholder="Paste Instagram Reel URL"
        className="
          w-full
          h-14
          rounded-2xl
          bg-[#111827]
          border
          border-white/10
          px-5
          outline-none
          focus:border-pink-500
        "
      />
    </div>

  </div>

  {/* ERROR */}
  {error && (
    <div className="rounded-2xl border border-red-500/20 bg-red-500/10 p-4 text-red-300">
      {error}
    </div>
  )}

  {/* BUTTON */}
  <button
    onClick={handleIngest}
    disabled={loading}
    className="
      w-full
      h-16
      rounded-[24px]
      font-bold
      text-lg
      bg-gradient-to-r
      from-cyan-500
      via-violet-500
      to-pink-500
      hover:shadow-[0_0_40px_rgba(168,85,247,.35)]
      transition-all
      duration-300
      disabled:opacity-60
    "
  >
    {loading
      ? "Analyzing Videos..."
      : "Generate AI Comparison"}
  </button>

  {/* RESULTS */}
  {(videoA || videoB) && (
    <>
      <div className="flex items-center gap-6">

        <div className="h-px flex-1 bg-white/10" />

        <div
          className="
          px-6
          py-3
          rounded-full
          bg-gradient-to-r
          from-cyan-500
          to-violet-500
          font-bold
          "
        >
          AI COMPARISON REPORT
        </div>

        <div className="h-px flex-1 bg-white/10" />

      </div>

      <div className="grid xl:grid-cols-2 gap-10">

        {videoA && (
          <VideoCard video={videoA} />
        )}

        {videoB && (
          <VideoCard video={videoB} />
        )}

      </div>
    </>
  )}
</div>


);
}
