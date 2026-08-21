import { Link } from "react-router-dom";

import { SampleMonitor } from "./SampleMonitor.jsx";

export function Hero() {
  return (
    <section className="mx-auto grid w-full max-w-5xl grid-cols-1 gap-10 px-6 py-16 sm:px-10 lg:grid-cols-[1.1fr_1fr] lg:items-center">
      <div className="fade-up">
        <p className="font-display text-[11px] font-medium tracking-[0.18em] text-rec">
          VIDEO INTELLIGENCE FOR SECURITY FOOTAGE
        </p>
        <h1 className="mt-3 font-display text-3xl font-semibold leading-tight text-text sm:text-4xl">
          Ask your footage what happened.
        </h1>
        <p className="mt-4 max-w-md font-body text-[15px] leading-relaxed text-text-dim">
          Sentinel watches a recording frame by frame, describes what it sees in detail, and
          answers plain-language questions about it — with timestamps pointing back into the
          clip, not guesses.
        </p>
        <Link
          to="/login"
          className="mt-6 inline-flex items-center gap-1.5 rounded-md bg-rec px-5 py-2.5 font-display text-[12px] font-medium tracking-wide text-white transition hover:bg-rec-deep"
        >
          OPEN THE CONSOLE
        </Link>
      </div>
      <div className="fade-up">
        <SampleMonitor />
      </div>
    </section>
  );
}
