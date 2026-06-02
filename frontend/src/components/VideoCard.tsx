import { VideoMetadata } from "../types";

interface Props {
  video: VideoMetadata;
}

export default function VideoCard({ video }: Props) {
  return (
    <div className="border rounded-lg p-5 shadow-sm bg-white hover:shadow-md transition">
      {/* TITLE */}
      <h2 className="font-bold text-lg mb-3">
        {video.title}
      </h2>

      {/* CREATOR + PLATFORM */}
      <div className="text-sm text-gray-700 mb-3">
        <p>
          <span className="font-medium">Creator:</span>{" "}
          {video.creator}
        </p>

        <p>
          <span className="font-medium">Platform:</span>{" "}
          {video.platform}
        </p>
      </div>

      {/* METRICS */}
      <div className="text-sm space-y-1">
        <p>
          <span className="font-medium">Views:</span>{" "}
          {video.views ?? 0}
        </p>

        <p>
          <span className="font-medium">Likes:</span>{" "}
          {video.likes ?? 0}
        </p>

        <p>
          <span className="font-medium">Comments:</span>{" "}
          {video.comments ?? 0}
        </p>

        <p>
          <span className="font-medium">Engagement:</span>{" "}
          {video.engagement_rate?.toFixed(2) ?? 0}%
        </p>
      </div>

      {/* HASHTAGS */}
      {video.hashtags?.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-1">
          {video.hashtags.map((tag, idx) => (
            <span
              key={idx}
              className="text-xs bg-gray-100 px-2 py-1 rounded"
            >
              #{tag}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}