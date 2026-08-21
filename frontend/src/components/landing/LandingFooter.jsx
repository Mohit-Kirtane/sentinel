export function LandingFooter() {
  return (
    <footer className="border-t border-line px-6 py-8 sm:px-10">
      <div className="mx-auto flex max-w-5xl flex-wrap items-center justify-between gap-3">
        <p className="font-display text-[11px] tracking-wide text-text-dim">SENTINEL</p>
        <a
          href="https://github.com/Mohit-Kirtane/sentinel"
          target="_blank"
          rel="noreferrer"
          className="font-body text-sm text-text-dim transition hover:text-text"
        >
          View code
        </a>
      </div>
    </footer>
  );
}
