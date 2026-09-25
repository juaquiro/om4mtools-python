#!/usr/bin/env bash
# download_data_fixtures.sh – Download every file from a public Dropbox
# *folder* link into a fresh local tests/data directory.
#
# CONFIGURATION ---------------------------------------------------------------
# 1. Copy the public ("Can view") **folder** link from Dropbox:
#      https://www.dropbox.com/sh/<share-id>/<access-token>
# 2. Paste it between the quotation marks of DROPBOX_URL below.
# 3. Run this script with no arguments, from anywhere:
#      ./download_data_fixtures.sh
#
# BEHAVIOUR -------------------------------------------------------------------
# • Always downloads into tests/data, relative to this script's location.
# • If tests/data already exists, the script asks for confirmation before
#   deleting it so you start with a completely clean copy of the folder.
# • Uses the ?dl=1 trick so Dropbox serves a single ZIP file containing the
#   whole folder, then unpacks it.
# • Prefers **bsdtar** for extraction (no spurious warnings). Falls back to
#   **unzip** and filters harmless "stripped absolute path spec" / "mapname"
#   messages from its output.
# -----------------------------------------------------------------------------

set -euo pipefail
IFS=$'\n\t'

### EDIT YOUR DROPBOX LINK HERE ###############################################

DROPBOX_URL="https://www.dropbox.com/scl/fo/530mljqql8r4ys6s1rwzp/ADYqbOQYrITmzqWgm-EkJI8?rlkey=nz4bfkn8n2zgmvsi162s969yo&dl=0"  # <- Replace this!

if [[ "$DROPBOX_URL" == *"<share-id>"* ]]; then
  echo "❌  DROPBOX_URL is still the placeholder – please edit the script and paste your real folder link." >&2
  exit 1
fi

### Destination directory #####################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST_DIR="$SCRIPT_DIR/tests/data"

# Start with a clean destination, but never silently discard local files
# (e.g. hand-authored fixtures/scripts not part of the Dropbox bundle).
if [[ -d "$DEST_DIR" ]]; then
  read -r -p "⚠️  '$DEST_DIR' already exists and will be deleted before re-downloading. Continue? [y/N] " REPLY
  if [[ ! "$REPLY" =~ ^[Yy]$ ]]; then
    echo "Aborted." >&2
    exit 1
  fi
  echo "🗑️  Removing previous '$DEST_DIR' directory …"
  rm -rf "$DEST_DIR"
fi
mkdir -p "$DEST_DIR"

### Ensure direct-download mode ###############################################

if [[ "$DROPBOX_URL" != *"dl=1"* ]]; then
  if [[ "$DROPBOX_URL" == *"?"* ]]; then
    DROPBOX_URL="${DROPBOX_URL}&dl=1"
  else
    DROPBOX_URL="${DROPBOX_URL}?dl=1"
  fi
fi

### Temporary ZIP file ########################################################

TEMP_ZIP="$(mktemp -t dropbox_folder_XXXX.zip)"  # create in /tmp

# Guarantee the temp archive is removed however the script exits — success,
# a failed download, or a failed extraction — not just on the happy path.
trap 'rm -f "$TEMP_ZIP"' EXIT

### Download ------------------------------------------------------------------

echo "⬇️  Downloading folder …"
curl --fail -L "$DROPBOX_URL" -o "$TEMP_ZIP"

### Extract -------------------------------------------------------------------

echo "📦 Extracting into '$DEST_DIR' …"

# ──────────────────────────────────────────────────────────────────────────────
#  We want to extract the ZIP archive quietly *and* avoid unnecessary warnings.
#
#  1) **bsdtar** (from libarchive / BSD tar) is the best tool: it understands
#     a wide range of character encodings, keeps permissions, and is far less
#     chatty than unzip. If it exists on the system we use it.
#
#       command -v bsdtar   →  prints the path to bsdtar if found, otherwise
#                              returns non‑zero status. We redirect both stdout
#                              and stderr to /dev/null so the check is silent.
#
#  2) If bsdtar is *not* available we fall back to classic **unzip**. unzip’s
#     output, however, often includes two benign but confusing warnings:
#         • "warning:  stripped absolute path spec from /…"
#         • "mapname:  conversion of  failed"
#     They merely indicate that unzip is discarding an absolute leading slash
#     (for safety) and that it can’t guess a filename’s charset. They do NOT
#     affect the extracted files.
#
#     We pipe unzip’s stderr/stdout through grep -Ev to filter out just those
#     warning lines, keeping the console output clean. The trailing "|| true"
#     ensures that the pipeline’s exit status doesn’t stop the script if grep
#     finds nothing to filter (–E = extended regex, -v = inverse match).
# ──────────────────────────────────────────────────────────────────────────────

if command -v bsdtar >/dev/null 2>&1; then
  # ── Preferred extractor ────────────────────────────────────────────────────
  bsdtar -xf "$TEMP_ZIP" -C "$DEST_DIR"
else
  # ── Fallback: unzip with noise suppression ─────────────────────────────────
  unzip -q "$TEMP_ZIP" -d "$DEST_DIR" 2>&1 | \
    grep -Ev '^(warning:  stripped absolute path spec|mapname:  conversion of)' || true
fi

### Cleanup -------------------------------------------------------------------
# Handled by the EXIT trap set above, so it runs on failure too.

echo "✅ All files are now in '$DEST_DIR'"
