import { Source } from "../types";

interface Props {
  source: Source;
}

export default function SourceCitation({ source }: Props) {
  return (
    <div className="text-xs border rounded p-2 bg-gray-50">
      <p>
        <span className="font-medium">Video:</span>{" "}
        {source.video_id}
      </p>

      <p>
        <span className="font-medium">Platform:</span>{" "}
        {source.platform}
      </p>

      <p>
        <span className="font-medium">Creator:</span>{" "}
        {source.creator}
      </p>
    </div>
  );
}