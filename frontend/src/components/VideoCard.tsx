import { VideoMetadata } from "../types";

interface Props {
video: VideoMetadata;
}

export default function VideoCard({ video }: Props) {
const formatNumber = (num?: number) => {
if (!num) return "0";


return Intl.NumberFormat("en-IN").format(num);


};

const engagement = Number(
video.engagement_rate || 0
).toFixed(2);

const isYoutube =
video.platform?.toLowerCase().includes("youtube");

return ( <div
   className="
   group
   relative
   overflow-hidden
   rounded-[32px]
   border
   border-white/10
   bg-[#0B1220]
   hover:border-cyan-500/30
   transition-all
   duration-500
   "
 >
<div
className={`         absolute
        top-0
        left-0
        w-full
        h-1
        ${
          isYoutube
            ? "bg-gradient-to-r from-red-500 to-orange-500"
            : "bg-gradient-to-r from-pink-500 to-violet-500"
        }
      `}
/>


  <div className="p-8">

    <div className="flex items-start justify-between mb-6">

      <div>

        <div
          className={`
          inline-flex
          px-3
          py-1
          rounded-full
          text-xs
          font-semibold
          mb-4
          ${
            isYoutube
              ? "bg-red-500/10 text-red-300"
              : "bg-pink-500/10 text-pink-300"
          }
        `}
        >
          {video.platform}
        </div>

        <h2 className="text-2xl font-bold leading-tight">
          {video.title}
        </h2>

      </div>

    </div>

    <div className="mb-8">

      <p className="text-slate-500 text-sm">
        Creator
      </p>

      <h3 className="text-lg font-semibold mt-1">
        {video.creator}
      </h3>

    </div>

    <div className="grid grid-cols-2 gap-4">

      <div className="rounded-2xl bg-white/[0.03] border border-white/5 p-5">
        <p className="text-slate-400 text-sm">
          Views
        </p>

        <h4 className="text-3xl font-bold mt-2">
          {formatNumber(video.views)}
        </h4>
      </div>

      <div className="rounded-2xl bg-white/[0.03] border border-white/5 p-5">
        <p className="text-slate-400 text-sm">
          Likes
        </p>

        <h4 className="text-3xl font-bold mt-2">
          {formatNumber(video.likes)}
        </h4>
      </div>

      <div className="rounded-2xl bg-white/[0.03] border border-white/5 p-5">
        <p className="text-slate-400 text-sm">
          Comments
        </p>

        <h4 className="text-3xl font-bold mt-2">
          {formatNumber(video.comments)}
        </h4>
      </div>

      <div className="rounded-2xl bg-white/[0.03] border border-white/5 p-5">
        <p className="text-slate-400 text-sm">
          Engagement
        </p>

        <h4 className="text-3xl font-bold mt-2 text-cyan-400">
          {engagement}%
        </h4>
      </div>

    </div>

    {video.followers && (
      <div className="mt-5 rounded-2xl bg-gradient-to-r from-cyan-500/10 to-violet-500/10 border border-cyan-500/10 p-5">
        <p className="text-slate-400 text-sm">
          Followers
        </p>

        <h4 className="text-3xl font-bold mt-2">
          {formatNumber(video.followers)}
        </h4>
      </div>
    )}

    {video.hashtags?.length > 0 && (
      <div className="mt-6">

        <p className="text-slate-500 text-sm mb-3">
          Hashtags
        </p>

        <div className="flex flex-wrap gap-2">

          {video.hashtags.map((tag, idx) => (
            <span
              key={idx}
              className="
              px-3
              py-1
              rounded-full
              bg-white/[0.03]
              border
              border-white/10
              text-sm
              "
            >
              #{tag}
            </span>
          ))}

        </div>

      </div>
    )}

  </div>
</div>


);
}
