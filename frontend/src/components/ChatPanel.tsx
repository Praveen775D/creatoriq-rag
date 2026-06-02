"use client";

import { useState } from "react";
import { askQuestion } from "../services/api";
import { Source } from "../types";

export default function ChatPanel() {
const [question, setQuestion] = useState("");
const [answer, setAnswer] = useState("");
const [sources, setSources] = useState<Source[]>([]);
const [loading, setLoading] = useState(false);

const suggestions = [
"Why did Video A outperform Video B?",
"Compare the first 5 seconds",
"What's the engagement rate?",
"Suggest improvements for Video B",
];

async function handleAsk() {
if (!question.trim()) return;

try {
  setLoading(true);

  const res = await askQuestion(
    question,
    "creator-session"
  );

  setAnswer(res?.answer || "");
  setSources(res?.sources || []);
} catch (err) {
  console.error(err);

  setAnswer(
    "Unable to generate a response at the moment."
  );

  setSources([]);
} finally {
  setLoading(false);
}


}

return ( <div className="space-y-8">

  {/* Suggested Prompts */}
  <div>
    <h3 className="text-sm uppercase tracking-wider text-slate-400 mb-4">
      Suggested Questions
    </h3>

    <div className="flex flex-wrap gap-3">
      {suggestions.map((item) => (
        <button
          key={item}
          onClick={() => setQuestion(item)}
          className="
            px-4
            py-2
            rounded-full
            border
            border-white/10
            bg-white/[0.03]
            hover:border-cyan-500/40
            hover:bg-cyan-500/10
            transition-all
            text-sm
          "
        >
          {item}
        </button>
      ))}
    </div>
  </div>

  {/* Question Input */}
  <div className="space-y-5">

    <textarea
      value={question}
      onChange={(e) => setQuestion(e.target.value)}
      placeholder="Ask anything about the videos..."
      className="
        w-full
        min-h-[180px]
        rounded-[28px]
        bg-[#111827]
        border
        border-white/10
        p-6
        text-white
        resize-none
        outline-none
        focus:border-cyan-500
        focus:ring-4
        focus:ring-cyan-500/10
        transition
      "
    />

    <button
      onClick={handleAsk}
      disabled={loading}
      className="
        w-full
        h-14
        rounded-2xl
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
        : "Generate AI Analysis"}
    </button>

  </div>

  {/* AI Response */}
  {answer && (
    <div
      className="
        rounded-[32px]
        border
        border-cyan-500/20
        bg-gradient-to-br
        from-cyan-500/5
        via-violet-500/5
        to-pink-500/5
        p-8
      "
    >

      <div className="flex items-center gap-4 mb-6">

        <div
          className="
            h-14
            w-14
            rounded-2xl
            bg-gradient-to-r
            from-cyan-500
            to-violet-500
            flex
            items-center
            justify-center
            text-2xl
          "
        >
          
        </div>

        <div>
          <h3 className="text-xl font-bold">
            CreatorIQ Analysis
          </h3>

          <p className="text-slate-400 text-sm">
            Generated using Retrieval-Augmented Generation
          </p>
        </div>

      </div>

      <div className="text-slate-200 whitespace-pre-wrap leading-8 text-[15px]">
        {answer}
      </div>

    </div>
  )}

  {/* Sources */}
  {sources.length > 0 && (
    <div>

      <div className="flex items-center justify-between mb-5">
        <h3 className="text-xl font-bold">
          Source Citations
        </h3>

        <span className="text-sm text-slate-400">
          {sources.length} Sources
        </span>
      </div>

      <div className="grid md:grid-cols-3 gap-5">

        {sources.map((source, index) => (
          <div
            key={`${source.video_id}-${index}`}
            className="
              rounded-[28px]
              border
              border-white/10
              bg-[#111827]
              p-5
              hover:border-cyan-500/40
              hover:-translate-y-1
              transition-all
            "
          >

            <div className="flex justify-between mb-4">

              <span className="px-3 py-1 rounded-full text-xs bg-cyan-500/10 text-cyan-300">
                {source.platform}
              </span>

              <span className="px-3 py-1 rounded-full text-xs bg-violet-500/10 text-violet-300">
                {source.video_id}
              </span>

            </div>

            <p className="text-slate-500 text-xs uppercase mb-1">
              Creator
            </p>

            <h4 className="font-semibold text-white">
              {source.creator}
            </h4>

          </div>
        ))}

      </div>

    </div>
  )}
</div>

);
}
