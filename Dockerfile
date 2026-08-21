FROM node:20-slim AS frontend-builder
WORKDIR /src
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
# Install the CPU-only PyTorch wheel first: the default PyPI build bundles
# CUDA/GPU libraries (several GB) that are never used on this CPU-only
# deployment and blow past Render's free-tier image size limit. sentence-
# transformers (for local embeddings) only needs torch>=1.11.0, so this
# satisfies that once installed and the rest of requirements.txt won't
# override it. Same fix as Dossier's Dockerfile.
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/app ./app
COPY --from=frontend-builder /src/dist ./app/static
ENV PORT=8000
EXPOSE 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
