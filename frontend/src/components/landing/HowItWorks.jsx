const STEPS = [
  {
    n: "01",
    title: "Watch",
    text: "Footage is sampled frame by frame and every person or object in view is detected and described in detail.",
  },
  {
    n: "02",
    title: "Remember",
    text: "Descriptions are merged into a timestamped timeline and indexed, so any moment in the footage is searchable.",
  },
  {
    n: "03",
    title: "Answer",
    text: "Ask a plain-language question and get an answer grounded in the timeline, citing exactly when it happened.",
  },
];

export function HowItWorks() {
  return (
    <section id="how-it-works" className="mx-auto w-full max-w-5xl px-6 py-14 sm:px-10">
      <div className="mb-8 border-b border-line pb-4">
        <p className="font-display text-[11px] font-medium tracking-[0.18em] text-rec">
          HOW IT WORKS
        </p>
      </div>
      <div className="grid grid-cols-1 gap-8 sm:grid-cols-3">
        {STEPS.map((step) => (
          <div key={step.n}>
            <span className="font-display text-[11px] text-timestamp">{step.n}</span>
            <h3 className="mt-2 font-display text-base font-semibold text-text">{step.title}</h3>
            <p className="mt-2 font-body text-sm leading-relaxed text-text-dim">{step.text}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
