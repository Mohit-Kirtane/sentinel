import { useEffect, useRef, useState } from "react";

import { listVideos } from "../api/client.js";
import { useAuth } from "../auth/AuthContext.jsx";
import { ChatPanel } from "../components/ChatPanel.jsx";
import { VideoPicker } from "../components/VideoPicker.jsx";
import { VideoPlayer } from "../components/VideoPlayer.jsx";

export default function DashboardPage() {
  const [videos, setVideos] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const playerRef = useRef(null);
  const { signOut } = useAuth();

  useEffect(() => {
    listVideos().then((result) => {
      setVideos(result);
      if (result.length > 0) setSelectedId(result[0].id);
    });
  }, []);

  const selectedVideo = videos.find((v) => v.id === selectedId) ?? null;

  function handleSeek(startTs) {
    if (playerRef.current) {
      playerRef.current.currentTime = startTs;
      playerRef.current.play();
    }
  }

  return (
    <div className="min-h-screen bg-bg">
      <header className="flex items-center justify-between border-b border-line px-6 py-4">
        <div>
          <h1 className="font-display text-lg font-semibold tracking-wide text-text">SENTINEL</h1>
          <p className="mt-0.5 font-body text-sm text-text-dim">
            Ask questions about security footage, grounded in detailed scene descriptions.
          </p>
        </div>
        <button
          onClick={signOut}
          className="rounded-md border border-line px-3 py-1.5 font-display text-[11px] tracking-wide text-text-dim transition hover:border-rec-deep hover:text-text"
        >
          SIGN OUT
        </button>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-8">
        <VideoPicker videos={videos} selectedId={selectedId} onSelect={setSelectedId} />

        <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-[1.3fr_1fr]">
          <VideoPlayer ref={playerRef} video={selectedVideo} />
          <div className="h-[420px] lg:h-auto">
            <ChatPanel videoId={selectedId} onSeek={handleSeek} />
          </div>
        </div>
      </main>
    </div>
  );
}
