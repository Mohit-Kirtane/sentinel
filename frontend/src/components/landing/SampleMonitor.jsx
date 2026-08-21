// Real output from Sentinel's own pipeline, run against a real ~9s clip of a
// street intersection (frame sampling -> YOLOv8n region detection -> NVIDIA
// DAM-3B-Video description -> pgvector retrieval -> Gemini). Not mocked.
const OBSERVED = [
  "A silver compact hatchback car with a sleek, modern design.",
  "A green and yellow auto rickshaw with a yellow canopy roof.",
  "A motorcyclist wearing a light blue long-sleeve shirt and dark pants.",
];

const SAMPLE_QUESTION = "What vehicles are visible in this footage?";
const SAMPLE_ANSWER =
  "Based on the scene descriptions, the following vehicles appear: Cars — a silver compact hatchback, a white hatchback with a roof rack, and a silver sedan. Rickshaws — a three-wheeled rickshaw and two auto-rickshaws, one green-and-yellow. Motorcycles — a dark, modern motorcycle. Bicycles — several, with varying frame colors.";

export function SampleMonitor() {
  return (
    <div className="relative overflow-hidden rounded-lg border border-line bg-surface">
      <div className="absolute inset-0 overflow-hidden">
        <div className="scan-sweep absolute inset-x-0 h-1/3 bg-gradient-to-b from-transparent via-rec/5 to-transparent" />
      </div>
      <div className="relative flex items-center justify-between border-b border-line px-3 py-2">
        <div className="flex items-center gap-2">
          <span className="rec-pulse h-2 w-2 rounded-full bg-rec" />
          <span className="font-display text-[11px] tracking-[0.14em] text-rec">REC</span>
          <span className="font-display text-[11px] tracking-wide text-text-dim">
            Street Intersection Camera
          </span>
        </div>
        <span className="rounded border border-timestamp/40 bg-timestamp/10 px-1.5 py-0.5 font-display text-[9px] tracking-wide text-timestamp">
          REAL OUTPUT
        </span>
      </div>
      <div className="relative space-y-2 p-4">
        {OBSERVED.map((text) => (
          <div key={text} className="flex gap-3 font-body text-sm">
            <span className="shrink-0 font-display text-[11px] text-timestamp">0:00–0:10</span>
            <span className="text-text-dim">{text}</span>
          </div>
        ))}
      </div>
      <div className="relative border-t border-line p-4">
        <p className="font-body text-sm text-text">
          <span className="text-text-dim">You asked: </span>"{SAMPLE_QUESTION}"
        </p>
        <p className="mt-2 font-body text-sm text-text-dim">{SAMPLE_ANSWER}</p>
      </div>
    </div>
  );
}
