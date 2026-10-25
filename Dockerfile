FROM python:3.14-alpine@sha256:601e99e090cb08c2784a42395487709500bc39930307fe72f3f11a8f3c430762 AS dependencies
WORKDIR /build
COPY requirements.lock .
RUN python -m pip install --no-cache-dir --only-binary=:all: --require-hashes --prefix=/install -r requirements.lock

FROM python:3.14-alpine@sha256:601e99e090cb08c2784a42395487709500bc39930307fe72f3f11a8f3c430762 AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=/app/src
WORKDIR /app
RUN python -m pip uninstall --yes pip && rm -rf /usr/local/lib/python3.14/ensurepip
COPY --from=dependencies /install /usr/local
COPY --chown=10001:10001 src/ ./src/
USER 10001:10001
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/healthz', timeout=3)"]
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--access-logfile", "-", "release_gate:create_app()"]
