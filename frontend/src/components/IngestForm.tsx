"use client";

import { useState } from "react";

import { ingestVideos }
from "@/services/api";

import VideoCard
from "./VideoCard";

export default function IngestForm() {

  const [youtubeUrl, setYoutubeUrl] =
    useState("");

  const [instagramUrl, setInstagramUrl] =
    useState("");

  const [videoA, setVideoA] =
    useState<any>(null);

  const [videoB, setVideoB] =
    useState<any>(null);

  async function handleIngest() {

    const data =
      await ingestVideos(
        youtubeUrl,
        instagramUrl
      );

    setVideoA(data.video_a);
    setVideoB(data.video_b);
  }

  return (
    <div>

      <input
        placeholder="YouTube URL"
        value={youtubeUrl}
        onChange={(e) =>
          setYoutubeUrl(e.target.value)
        }
        className="border p-2 w-full"
      />

      <input
        placeholder="Instagram URL"
        value={instagramUrl}
        onChange={(e) =>
          setInstagramUrl(e.target.value)
        }
        className="border p-2 w-full mt-2"
      />

      <button
        onClick={handleIngest}
        className="border px-4 py-2 mt-2"
      >
        Analyze Videos
      </button>

      <div className="grid grid-cols-2 gap-4 mt-4">

        {videoA &&
          <VideoCard video={videoA} />
        }

        {videoB &&
          <VideoCard video={videoB} />
        }

      </div>

    </div>
  );
}