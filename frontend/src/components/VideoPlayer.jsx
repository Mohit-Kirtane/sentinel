import { forwardRef } from "react";

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
      <div className="flex items-center gap-2 border-b border-line px-3 py-2">
        <span className="rec-pulse h-2 w-2 rounded-full bg-rec" />
        <span className="font-display text-[11px] tracking-[0.14em] text-rec">REC</span>
        <span className="font-display text-[11px] tracking-wide text-text-dim">{video.title}</span>
      </div>
      <video
        ref={ref}
        src={`/demo-videos/${video.filename}`}
        controls
        className="aspect-video w-full bg-black"
      />
    </div>
  );
});
