import { Link } from "react-router-dom";

import { PortfolioMark } from "../icons/PortfolioMark.jsx";

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
          <a href="#features" className="transition hover:text-text">
            Features
          </a>
        </nav>
        <div className="flex items-center gap-3">
          <a
            href="https://portfolio-mohit-kirtane.vercel.app/"
            target="_blank"
            rel="noreferrer"
            title="Mohit Kirtane's portfolio"
            className="text-text-dim transition hover:text-rec"
          >
            <PortfolioMark className="h-4 w-4" />
          </a>
          <Link
            to="/login"
            className="rounded-md bg-rec px-4 py-2 font-display text-[12px] font-medium tracking-wide text-white transition hover:bg-rec-deep"
          >
            SIGN IN
          </Link>
        </div>
      </div>
    </header>
  );
}
