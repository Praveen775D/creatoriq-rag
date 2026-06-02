"use client";

import { useState } from "react";
import { askQuestion } from "../services/api";
import { Source } from "../types";

export default function ChatPanel() {
  const [question, setQuestion] = useState<string>("");
  const [answer, setAnswer] = useState<string>("");
  const [sources, setSources] = useState<Source[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  async function handleAsk() {
    const trimmed = question.trim();

    if (!trimmed) return;

    try {
      setLoading(true);

      const res = await askQuestion(
        trimmed,
        "creator-session"
      );

      setAnswer(res?.answer ?? "");
      setSources(res?.sources ?? []);
    } catch (err) {
      console.error("Chat error:", err);
      setAnswer("Something went wrong while fetching response.");
      setSources([]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="border rounded-lg p-5 bg-white shadow-sm">
      <h2 className="text-xl font-semibold mb-4">
        CreatorIQ RAG Chat
      </h2>

      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask: Why did Video A perform better than Video B?"
        className="w-full border rounded p-3 min-h-[120px] focus:outline-none focus:ring-2 focus:ring-blue-400"
      />

      <button
        onClick={handleAsk}
        disabled={loading}
        className={`mt-3 px-4 py-2 rounded border transition ${
          loading ? "opacity-60 cursor-not-allowed" : "hover:bg-gray-100"
        }`}
      >
        {loading ? "Thinking..." : "Ask Question"}
      </button>

      {/* ANSWER SECTION */}
      {answer && (
        <div className="mt-6">
          <h3 className="font-semibold mb-2">Answer</h3>
          <div className="border rounded p-3 whitespace-pre-wrap bg-gray-50">
            {answer}
          </div>
        </div>
      )}

      {/* SOURCES SECTION */}
      {sources.length > 0 && (
        <div className="mt-6">
          <h3 className="font-semibold mb-2">Sources</h3>

          <div className="space-y-2">
            {sources.map((source, idx) => (
              <div
                key={`${source.video_id}-${idx}`}
                className="border rounded p-3 text-sm bg-white"
              >
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
            ))}
          </div>
        </div>
      )}
    </div>
  );
}