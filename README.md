# Sentinel

A video-intelligence chatbot for security footage: ask natural-language
questions about a video and get answers grounded in detailed scene
descriptions, with timestamp citations that seek the player.

## Architecture

Two decoupled halves. An **offline enrichment pipeline** (`pipeline/`),
run manually per demo video in a GPU notebook (Colab/Kaggle) alongside a
locally-started [DAM server](https://github.com/NVlabs/describe-anything)
- never deployed:

```
video.mp4
  -> ffmpeg: sample a frame every N seconds, with timestamps
  -> YOLOv8n: propose person/object regions per sampled frame
  -> DAM: detailed description per region (via its OpenAI-compatible API)
  -> segment builder: merge per-frame region descriptions into
     fixed-width time windows -> one paragraph per segment
  -> Gemini embeddings: embed each segment's text
  -> Postgres (pgvector): store videos + segments
```

And a **live app** (`backend/` + `frontend/`), deployed as a single
Render web service, entirely CPU-only at request time - it only ever
reads what the offline pipeline already wrote:

```
user signs in (single seeded demo account)
  -> picks a precomputed video
  -> asks a question
  -> backend embeds the question (Gemini)
  -> pgvector: ORDER BY embedding <=> query_embedding LIMIT k,
     filtered to matches above a similarity threshold
  -> Gemini: synthesize an answer from the retrieved segments,
     citing timestamps
  -> frontend renders the answer with clickable timestamp chips
```

v1 deliberately excludes: live/streaming video, cross-frame person
re-identification, audio/speech transcription, automated anomaly
alerting, and public video upload (the video set is fixed and
precomputed).

## Running locally

Backend:

```bash
cd backend
pip install -r requirements.txt
cp ../.env.example .env
# edit .env: DATABASE_URL (a pgvector-enabled Postgres - Neon's free
# tier works) and LLM_API_KEY (https://aistudio.google.com/apikey)
uvicorn app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Tests (pipeline logic + backend API, both mocked against fakes rather
than real external services - see the design spec for why):

```bash
pip install -r backend/requirements.txt -r pipeline/requirements.txt pytest pytest-asyncio
pytest
```

## Adding a demo video

1. Drop the clip into `frontend/public/demo-videos/<name>.mp4`.
2. In a GPU notebook, start the DAM server
   ([`dam_server.py`](https://github.com/NVlabs/describe-anything/blob/main/dam_server.py))
   and run:

   ```bash
   pip install -r pipeline/requirements.txt
   python -m pipeline.run_pipeline \
     --video frontend/public/demo-videos/<name>.mp4 \
     --video-id <name> \
     --title "Human-readable title" \
     --dam-server-url http://localhost:8000 \
     --frame-skip 2
   ```

   `--frame-skip N` only sends every Nth *extracted* frame through DAM (the
   expensive step) - consecutive sampled frames of a mostly-static scene are
   highly redundant, so this cuts real cost/time independently of
   `--interval-seconds`' own sampling rate.

3. Redeploy the frontend with the new clip committed.

## Deployment

Single Docker image serves the API and the built React dashboard (same
pattern as Dossier/Tracewell). [`render.yaml`](render.yaml) defines one
web service, `sentinel-api`.

1. Provision a free Neon Postgres database (persistent, unlike Render's
   own free Postgres which expires after 30 days) with the `vector`
   extension enabled.
2. On Render: **New → Blueprint**, point it at this repo.
3. Fill in the `sync: false` env vars: `DATABASE_URL` (from Neon) and
   `LLM_API_KEY` (from
   [Google AI Studio](https://aistudio.google.com/apikey)). `JWT_SECRET`
   is auto-generated. Users register their own account from the
   landing page - no seeded credentials needed.
4. Run the offline pipeline against at least one demo video before
   relying on the live chat - without precomputed segments, the app has
   videos listed but nothing for the chatbot to answer from.
