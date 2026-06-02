import { Source } from "../types";

interface Props {
  source: Source;
}

export default function SourceCitation({ source }: Props) {
  return (
    <div className="group rounded-xl border border-gray-100 bg-white p-3 shadow-sm transition hover:shadow-md">

      {/* HEADER ROW */}
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold text-gray-500">
          Source
        </span>

        <span className="rounded-full bg-black px-2 py-0.5 text-[10px] font-medium text-white">
          {source.platform}
        </span>
      </div>

      {/* VIDEO ID */}
      <div className="mt-2">
        <p className="text-[11px] text-gray-500">Video ID</p>
        <p className="mt-1 inline-block rounded-md bg-gray-100 px-2 py-1 text-xs font-medium text-gray-800 group-hover:bg-gray-200 transition">
          {source.video_id}
        </p>
      </div>

      {/* CREATOR */}
      <div className="mt-2">
        <p className="text-[11px] text-gray-500">Creator</p>
        <p className="text-sm font-medium text-gray-900">
          {source.creator}
        </p>
      </div>
    </div>
  );
}