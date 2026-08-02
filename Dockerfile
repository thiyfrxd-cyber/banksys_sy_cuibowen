# ── banksys_sy_cuibowen Dockerfile ──
# Build:  docker build -t banksys_sy_cuibowen .
# Run:    docker run -d --name banksys_sy_cuibowen -p 8888:8501 banksys_sy_cuibowen

FROM python:3.11-slim

# Build-time args (before FROM declaration doesn't carry over — re-declare after)
ARG PIP_INDEX_URL=https://pypi.org/simple

WORKDIR /app

# ── 1. Install Python dependencies (no apt-get needed) ──
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 120 \
    --index-url "${PIP_INDEX_URL}" \
    -r requirements.txt

# ── 2. Copy application code and data ──
COPY app/ ./app/
COPY data/ ./data/

# ── 3. Train model during build (self-contained image) ──
# Use --overwrite to ensure fresh model; model saved to app/ml/model/
RUN python -m app.ml.train --overwrite

# ── 4. Ensure app package is importable from /app ──
ENV PYTHONPATH=/app

# ── 5. Streamlit port ──
EXPOSE 8501

# ── 6. Healthcheck using Python (no curl → no apt-get timeout on CN servers) ──
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

# ── 7. Launch ──
CMD ["streamlit", "run", "app/main.py", \
     "--server.address=0.0.0.0", \
     "--server.port=8501", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]
