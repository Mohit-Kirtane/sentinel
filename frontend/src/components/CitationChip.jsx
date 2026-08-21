function formatTimestamp(seconds) {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60)
    .toString()
    .padStart(2, "0");
  return `${m}:${s}`;
}

export function CitationChip({ citation, onSeek }) {
  return (
    <button
      onClick={() => onSeek(citation.start_ts)}
      className="rounded border border-timestamp/40 bg-timestamp/10 px-2 py-0.5 font-display text-[11px] tracking-wide text-timestamp transition hover:bg-timestamp/20"
    >
      {formatTimestamp(citation.start_ts)}–{formatTimestamp(citation.end_ts)}
    </button>
  );
}
