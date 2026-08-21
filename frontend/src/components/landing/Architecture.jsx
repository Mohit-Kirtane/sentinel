export function Architecture() {
  return (
    <section className="mx-auto w-full max-w-5xl px-6 py-14 sm:px-10">
      <div className="mb-8 border-b border-line pb-4">
        <p className="font-display text-[11px] font-medium tracking-[0.18em] text-rec">
          HOW IT'S BUILT
        </p>
        <h2 className="mt-2 font-display text-xl font-semibold text-text">
          The expensive step runs once. The live app never touches a GPU.
        </h2>
      </div>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div className="rounded-lg border border-line bg-surface p-5">
          <p className="font-display text-[11px] tracking-[0.14em] text-timestamp">
            OFFLINE · GPU NOTEBOOK · ONCE PER VIDEO
          </p>
          <pre className="mt-3 overflow-x-auto font-display text-[12px] leading-relaxed text-text-dim">
            {`video.mp4
  -> ffmpeg: sample frames
  -> YOLOv8n: detect regions
  -> DAM-3B-Video: describe each
  -> merge + dedupe near-duplicates
  -> embed (sentence-transformers)
  -> Postgres (pgvector)`}
          </pre>
        </div>
        <div className="rounded-lg border border-line bg-surface p-5">
          <p className="font-display text-[11px] tracking-[0.14em] text-rec">
            LIVE · CPU ONLY · EVERY QUESTION
          </p>
          <pre className="mt-3 overflow-x-auto font-display text-[12px] leading-relaxed text-text-dim">
            {`your question
  -> embed (sentence-transformers)
  -> pgvector similarity search
  -> match? -> Gemini generates
             an answer, cites
             the timestamp
  -> no match? -> says so`}
          </pre>
        </div>
      </div>
    </section>
  );
}
