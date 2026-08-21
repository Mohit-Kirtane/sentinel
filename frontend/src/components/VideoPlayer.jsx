import { forwardRef, useEffect, useState } from "react";

function LiveClock() {
  const [now, setNow] = useState(() => new Date());

  useEffect(() => {
    const interval = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <span className="font-display text-[11px] tabular-nums text-text-dim">
      {now.toLocaleTimeString("en-US", { hour12: false })}
    </span>
  );
}

function CornerBrackets() {
  const corner = "absolute h-5 w-5 border-rec/70";
  return (
    <div className="pointer-events-none absolute inset-3">
      <div className={`${corner} left-0 top-0 border-l-2 border-t-2`} />
      <div className={`${corner} right-0 top-0 border-r-2 border-t-2`} />
      <div className={`${corner} bottom-0 left-0 border-b-2 border-l-2`} />
      <div className={`${corner} bottom-0 right-0 border-b-2 border-r-2`} />
    </div>
  );
}

export const VideoPlayer = forwardRef(function VideoPlayer({ video }, ref) {
  if (!video) {
    return (
      <div className="flex aspect-video items-center justify-center rounded-lg border border-line bg-surface font-display text-[12px] text-text-dim">
        SELECT A CAMERA TO BEGIN
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-lg border border-line bg-surface">
      <div className="flex items-center justify-between border-b border-line px-3 py-2">
        <div className="flex items-center gap-2">
          <span className="rec-pulse h-2 w-2 rounded-full bg-rec" />
          <span className="font-display text-[11px] tracking-[0.14em] text-rec">REC</span>
          <span className="font-display text-[11px] tracking-wide text-text-dim">{video.title}</span>
        </div>
        <LiveClock />
      </div>
      <div className="relative">
        <video
          ref={ref}
          src={`/demo-videos/${video.filename}`}
          controls
          className="aspect-video w-full bg-black"
        />
        <CornerBrackets />
      </div>
    </div>
  );
});
