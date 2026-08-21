import { Link } from "react-router-dom";

export function LandingHeader() {
  return (
    <header className="border-b border-line">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4 sm:px-10">
        <div className="flex items-center gap-2">
          <span className="rec-pulse h-2 w-2 rounded-full bg-rec" />
          <span className="font-display text-sm font-semibold tracking-[0.14em] text-text">
            SENTINEL
          </span>
        </div>
        <nav className="hidden items-center gap-7 font-body text-sm text-text-dim md:flex">
          <a href="#how-it-works" className="transition hover:text-text">
            How it works
          </a>
        </nav>
        <Link
          to="/login"
          className="rounded-md bg-rec px-4 py-2 font-display text-[12px] font-medium tracking-wide text-white transition hover:bg-rec-deep"
        >
          SIGN IN
        </Link>
      </div>
    </header>
  );
}
