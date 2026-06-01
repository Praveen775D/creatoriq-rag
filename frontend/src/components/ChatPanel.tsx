"use client";

import { useState } from "react";

import { askQuestion } from "../services/api";

interface Source {
  video_id: string;
  platform: string;
  creator: string;
}

export default function ChatPanel() {
  const [question, setQuestion] =
    useState("");

  const [answer, setAnswer] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [sources, setSources] =
    useState<Source[]>([]);

  async function handleAsk() {
    if (!question.trim()) {
      return;
    }

    try {
      setLoading(true);

      const data =
        await askQuestion(
          question,
          "creator-session"
        );

      setAnswer(
        data.answer || ""
      );

      setSources(
        data.sources || []
      );
    } catch (error) {
      console.error(error);

      setAnswer(
        "Failed to get response."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="border rounded-lg p-4 bg-white">
      <h2 className="text-xl font-bold mb-4">
        CreatorIQ RAG Chat
      </h2>

      <textarea
        value={question}
        onChange={(e) =>
          setQuestion(
            e.target.value
          )
        }
        placeholder="Ask about Video A and Video B..."
        className="border rounded p-3 w-full min-h-[120px]"
      />

      <button
        onClick={handleAsk}
        disabled={loading}
        className="mt-3 px-4 py-2 border rounded"
      >
        {loading
          ? "Thinking..."
          : "Ask Question"}
      </button>

      {answer && (
        <div className="mt-6">
          <h3 className="font-bold mb-2">
            Answer
          </h3>

          <div className="border rounded p-3 whitespace-pre-wrap">
            {answer}
          </div>
        </div>
      )}

      {sources.length > 0 && (
        <div className="mt-6">
          <h3 className="font-bold mb-2">
            Sources
          </h3>

          {sources.map(
            (
              source,
              index
            ) => (
              <div
                key={index}
                className="border rounded p-2 mb-2"
              >
                <p>
                  Video:
                  {" "}
                  {source.video_id}
                </p>

                <p>
                  Platform:
                  {" "}
                  {source.platform}
                </p>

                <p>
                  Creator:
                  {" "}
                  {source.creator}
                </p>
              </div>
            )
          )}
        </div>
      )}
    </div>
  );
}