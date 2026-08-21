const SAMPLE_LOG = [
  { ts: "0:04", text: "A person in a dark jacket enters the frame from the left." },
  { ts: "0:11", text: "The person sets a backpack down near the counter and steps away." },
  { ts: "0:19", text: "The person walks out of frame without the backpack." },
];

export function SampleMonitor() {
  return (
    <div className="relative overflow-hidden rounded-lg border border-line bg-surface">
      <div className="absolute inset-0 overflow-hidden">
        <div className="scan-sweep absolute inset-x-0 h-1/3 bg-gradient-to-b from-transparent via-rec/5 to-transparent" />
      </div>
      <div className="relative flex items-center gap-2 border-b border-line px-3 py-2">
        <span className="rec-pulse h-2 w-2 rounded-full bg-rec" />
        <span className="font-display text-[11px] tracking-[0.14em] text-rec">REC</span>
        <span className="font-display text-[11px] tracking-wide text-text-dim">Lobby Camera 02</span>
      </div>
      <div className="relative space-y-2 p-4">
        {SAMPLE_LOG.map((entry) => (
          <div key={entry.ts} className="flex gap-3 font-body text-sm">
            <span className="shrink-0 font-display text-[11px] text-timestamp">{entry.ts}</span>
            <span className="text-text-dim">{entry.text}</span>
          </div>
        ))}
      </div>
      <div className="relative border-t border-line p-4">
        <p className="font-body text-sm text-text">
          <span className="text-text-dim">You asked: </span>
          "Did anyone leave a bag near the counter?"
        </p>
        <p className="mt-2 font-body text-sm text-text">
          Yes — at <span className="rounded bg-timestamp/10 px-1.5 py-0.5 font-display text-[11px] text-timestamp">0:11</span> a
          person in a dark jacket left a backpack near the counter and walked away without it.
        </p>
      </div>
    </div>
  );
}
