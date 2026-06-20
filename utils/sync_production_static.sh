#!/usr/bin/env bash
set -euo pipefail

APP_ROOT="${APP_ROOT:-/home/toptuk/pmi.moscow}"
IMAGE="${1:?docker image tag is required, e.g. ghcr.io/toptuk/pmiclub:abc123}"
STATIC_DIR="${APP_ROOT}/frontend/static"

mkdir -p "${STATIC_DIR}"
CID="$(docker create "${IMAGE}")"
trap 'docker rm -f "${CID}" >/dev/null 2>&1 || true' EXIT

docker cp "${CID}:/app/frontend/static/." "${STATIC_DIR}/"
docker rm "${CID}"
trap - EXIT

MAIN_JS="$(find "${STATIC_DIR}/dist" -maxdepth 1 -name 'main-*.js' -print -quit)"
if [[ -z "${MAIN_JS}" ]]; then
  echo "Static sync failed: ${STATIC_DIR}/dist/main-*.js not found" >&2
  exit 1
fi

echo "Static files synced to ${STATIC_DIR} ($(basename "${MAIN_JS}"))"
