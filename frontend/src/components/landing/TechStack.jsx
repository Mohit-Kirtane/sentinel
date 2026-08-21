const STACK = ["FASTAPI", "POSTGRES/PGVECTOR", "LANGGRAPH", "YOLOV8N", "NVIDIA DAM", "REACT", "GEMINI"];

export function TechStack() {
  return (
    <section className="mx-auto w-full max-w-5xl px-6 py-10 sm:px-10">
      <div className="flex flex-wrap items-center gap-3 border-t border-line pt-8">
        <span className="mr-2 font-display text-[11px] tracking-[0.18em] text-text-dim">
          BUILT WITH
        </span>
        {STACK.map((name) => (
          <span
            key={name}
            className="rounded border border-line px-2.5 py-1 font-display text-[11px] tracking-wide text-text-dim"
          >
            {name}
          </span>
        ))}
      </div>
    </section>
  );
}
