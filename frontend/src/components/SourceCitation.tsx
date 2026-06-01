import { Source } from "@/types";

interface Props {
  source: Source;
}

export default function SourceCitation(
  { source }: Props
) {
  return (
    <div className="text-xs border rounded p-2">

      {source.source}

      {" | "}

      {source.platform}

    </div>
  );
}