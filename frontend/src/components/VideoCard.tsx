import { VideoMetadata } from "@/types";

interface Props {
  video: VideoMetadata;
}

export default function VideoCard(
  { video }: Props
) {
  return (
    <div className="border rounded-lg p-4 shadow">

      <h2 className="font-bold text-lg">
        {video.title}
      </h2>

      <p>
        Creator: {video.creator}
      </p>

      <p>
        Views: {video.views}
      </p>

      <p>
        Likes: {video.likes}
      </p>

      <p>
        Comments: {video.comments}
      </p>

      <p>
        Engagement:
        {" "}
        {video.engagement_rate}%
      </p>

    </div>
  );
}