import { VideoMetadata } from "../types";

interface Props {
  video: VideoMetadata;
}

export default function VideoCard({ video }: Props) {
  return (
    <div className="group relative rounded-2xl border border-gray-100 bg-white p-6 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-xl">
      
      {/* PLATFORM BADGE */}
      <div className="absolute right-4 top-4">
        <span className="rounded-full bg-black px-3 py-1 text-xs font-medium text-white">
          {video.platform}
        </span>
      </div>

      {/* TITLE */}
      <h2 className="mb-3 pr-16 text-lg font-bold leading-snug text-gray-900 group-hover:text-black">
        {video.title}
      </h2>

      {/* CREATOR */}
      <p className="mb-4 text-sm text-gray-600">
        <span className="font-medium text-gray-800">Creator:</span>{" "}
        {video.creator}
      </p>

      {/* METRICS GRID */}
      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-lg bg-gray-50 p-3">
          <p className="text-gray-500">Views</p>
          <p className="text-base font-semibold text-gray-900">
            {(video.views ?? 0).toLocaleString()}
          </p>
        </div>

        <div className="rounded-lg bg-gray-50 p-3">
          <p className="text-gray-500">Likes</p>
          <p className="text-base font-semibold text-gray-900">
            {(video.likes ?? 0).toLocaleString()}
          </p>
        </div>

        <div className="rounded-lg bg-gray-50 p-3">
          <p className="text-gray-500">Comments</p>
          <p className="text-base font-semibold text-gray-900">
            {(video.comments ?? 0).toLocaleString()}
          </p>
        </div>

        <div className="rounded-lg bg-gradient-to-br from-indigo-50 to-purple-50 p-3">
          <p className="text-gray-500">Engagement</p>
          <p className="text-base font-bold text-indigo-600">
            {video.engagement_rate?.toFixed(2) ?? "0.00"}%
          </p>
        </div>
      </div>

      {/* HASHTAGS */}
      {video.hashtags?.length > 0 && (
        <div className="mt-4 flex flex-wrap gap-2">
          {video.hashtags.map((tag, idx) => (
            <span
              key={idx}
              className="rounded-full bg-gray-100 px-3 py-1 text-xs text-gray-700 transition hover:bg-gray-200"
            >
              #{tag}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}