export function LandingFooter() {
  return (
    <footer className="border-t border-line px-6 py-8 sm:px-10">
      <div className="mx-auto flex max-w-5xl flex-col items-start justify-between gap-3 sm:flex-row sm:items-center">
        <p className="font-display text-[11px] tracking-wide text-text-dim">SENTINEL</p>
        <p className="font-display text-[11px] tracking-wide text-text-dim">
          BUILT BY{" "}
          <a
            href="https://github.com/Mohit-Kirtane"
            target="_blank"
            rel="noreferrer"
            className="text-text underline decoration-line underline-offset-2 transition hover:text-rec"
          >
            MOHIT KIRTANE
          </a>{" "}
          ·{" "}
          <a
            href="https://github.com/Mohit-Kirtane/sentinel"
            target="_blank"
            rel="noreferrer"
            className="text-text underline decoration-line underline-offset-2 transition hover:text-rec"
          >
            VIEW CODE
          </a>
        </p>
      </div>
    </footer>
  );
}
