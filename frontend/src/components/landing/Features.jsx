import { useEffect, useRef, useState } from "react";

const FEATURES = [
  {
    title: "Detailed, not just detected",
    text: "YOLOv8n finds every person and object in frame, then NVIDIA's DAM-3B-Video describes each one in detail — clothing, color, what it's doing — not just a label and a box.",
  },
  {
    title: "Grounded, cited answers",
    text: "Every answer is retrieved from what was actually observed in the footage via pgvector similarity search, and cites the exact timestamp — no match above the threshold means Sentinel says so, instead of guessing.",
  },
  {
    title: "GPU only where it's needed",
    text: "The expensive step (DAM inference) runs once, offline, in a GPU notebook. The live app that answers your questions is 100% CPU — no GPU bill for something that only needs to run once per video.",
  },
  {
    title: "A real RAG pipeline",
    text: "Retrieval and generation run as an actual LangGraph state machine — embed the question, retrieve matching scenes, route to generation or an honest \"nothing matches\", then answer.",
  },
];

function FeatureCard({ feature, index }) {
  const ref = useRef(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      setVisible(true);
      return;
    }
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setVisible(true);
          observer.disconnect();
        }
      },
      { threshold: 0.2 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return (
    <div
      ref={ref}
      style={{ transitionDelay: visible ? `${index * 80}ms` : "0ms" }}
      className={`rounded-lg border border-line bg-surface p-5 transition-all duration-500 ease-out hover:-translate-y-0.5 hover:border-rec-deep ${
        visible ? "translate-y-0 opacity-100" : "translate-y-3 opacity-0"
      }`}
    >
      <h3 className="font-display text-sm font-semibold text-text">{feature.title}</h3>
      <p className="mt-2 font-body text-sm leading-relaxed text-text-dim">{feature.text}</p>
    </div>
  );
}

export function Features() {
  return (
    <section id="features" className="mx-auto w-full max-w-5xl px-6 py-14 sm:px-10">
      <div className="mb-8 border-b border-line pb-4">
        <p className="font-display text-[11px] font-medium tracking-[0.18em] text-rec">FEATURES</p>
      </div>
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
        {FEATURES.map((feature, index) => (
          <FeatureCard key={feature.title} feature={feature} index={index} />
        ))}
      </div>
    </section>
  );
}
