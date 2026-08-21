import { useState } from "react";

import { askQuestion } from "../api/client.js";
import { CitationChip } from "./CitationChip.jsx";

function AnalyzingIndicator() {
  return (
    <div className="flex items-center gap-2 font-display text-[11px] tracking-[0.14em] text-text-dim">
      <span className="flex gap-0.5">
        <span className="rec-pulse h-1 w-1 rounded-full bg-rec [animation-delay:0ms]" />
        <span className="rec-pulse h-1 w-1 rounded-full bg-rec [animation-delay:200ms]" />
        <span className="rec-pulse h-1 w-1 rounded-full bg-rec [animation-delay:400ms]" />
      </span>
      ANALYZING FOOTAGE…
    </div>
  );
}

function MessageBubble({ message, onSeek }) {
  const isUser = message.role === "user";
  return (
    <div className={isUser ? "text-right" : "text-left"}>
      <p
        className={`font-display text-[10px] tracking-[0.14em] ${
          isUser ? "text-text-dim" : "text-rec"
        }`}
      >
        {isUser ? "YOU" : "SENTINEL"}
      </p>
      <p
        className={`mt-1 inline-block max-w-[85%] rounded-md px-3 py-2 font-body text-sm ${
          isUser ? "bg-surface-raised text-text" : "bg-transparent text-text"
        }`}
      >
        {message.text}
      </p>
      {message.citations && message.citations.length > 0 && (
        <div className="mt-1.5 flex flex-wrap justify-start gap-1.5">
          {message.citations.map((citation, i) => (
            <CitationChip key={i} citation={citation} onSeek={onSeek} />
          ))}
        </div>
      )}
    </div>
  );
}

const SUGGESTED_QUESTIONS = [
  "What vehicles are visible in this footage?",
  "Summarize what happens in this footage.",
  "What are the people in this footage wearing?",
];

export function ChatPanel({ videoId, onSeek }) {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function ask(asked) {
    if (!asked.trim() || !videoId) return;

    setMessages((prev) => [...prev, { role: "user", text: asked }]);
    setQuestion("");
    setLoading(true);
    setError(null);

    try {
      const result = await askQuestion(videoId, asked);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: result.answer, citations: result.citations },
      ]);
    } catch {
      setError("Something went wrong asking that question. Try again.");
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(event) {
    event.preventDefault();
    ask(question);
  }

  return (
    <div className="flex h-full flex-col rounded-lg border border-line bg-surface">
      <div className="flex items-center gap-2 border-b border-line px-3 py-2">
        <span className="rec-pulse h-2 w-2 rounded-full bg-rec" />
        <span className="font-display text-[11px] tracking-[0.14em] text-text">ANALYSIS LOG</span>
      </div>
      <div className="flex-1 space-y-4 overflow-y-auto p-4">
        {messages.length === 0 && (
          <div>
            <p className="font-body text-sm text-text-dim">
              Ask about what happens in this footage, or try one of these:
            </p>
            <div className="mt-3 flex flex-wrap gap-1.5">
              {SUGGESTED_QUESTIONS.map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => ask(suggestion)}
                  disabled={!videoId || loading}
                  className="rounded-md border border-line px-2.5 py-1 font-body text-xs text-text-dim transition hover:border-rec-deep hover:text-text disabled:opacity-40"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}
        {messages.map((message, index) => (
          <MessageBubble key={index} message={message} onSeek={onSeek} />
        ))}
        {loading && <AnalyzingIndicator />}
        {error && <p className="font-body text-sm text-rec">{error}</p>}
      </div>
      <form onSubmit={handleSubmit} className="flex gap-2 border-t border-line p-3">
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          disabled={!videoId || loading}
          placeholder={videoId ? "Ask a question about this footage…" : "Select a camera first"}
          className="flex-1 rounded-md border border-line bg-bg px-3 py-2 font-body text-sm text-text placeholder:text-text-dim focus:outline-none"
        />
        <button
          type="submit"
          disabled={!videoId || loading || !question.trim()}
          className="rounded-md bg-rec px-4 py-2 font-display text-[12px] font-medium tracking-wide text-white transition hover:bg-rec-deep disabled:opacity-40"
        >
          ASK
        </button>
      </form>
    </div>
  );
}
