export function VideoPicker({ videos, selectedId, onSelect }) {
  return (
    <div className="flex flex-wrap gap-2">
      {videos.map((video) => (
        <button
          key={video.id}
          onClick={() => onSelect(video.id)}
          className={`rounded-md border px-3 py-1.5 font-display text-[12px] tracking-wide transition ${
            video.id === selectedId
              ? "border-rec bg-rec/10 text-rec"
              : "border-line text-text-dim hover:border-rec-deep hover:text-text"
          }`}
        >
          {video.title}
        </button>
      ))}
    </div>
  );
}
