#!/usr/bin/env python3
"""Entry for u-alven-the-gps-swears-it-was-a-shortcut-2cac21d9.

Prints exactly the GPS excuse, a single line of plain text.
Deterministic, stdlib only: no network, clock, or randomness.
"""

import os
import sys
import tempfile

# Entry text: 132 characters, single line, no setup, no dialogue tags.
ENTRY = "I didn't send you down the wrong road \u2014 the shortcut was real, the map just forgot to mention the lake, the goats, and the dead end."


def main() -> int:
    if "\n" in ENTRY or "\r" in ENTRY:
        raise ValueError("entry must be a single line")
    if len(ENTRY) > 200:
        raise ValueError("entry exceeds 200 characters")
    if ENTRY != ENTRY.strip():
        raise ValueError("entry has stray whitespace")
    # Verify by staging to a temp file and reading it back.
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as tmp:
        tmp_path = tmp.name
        tmp.write(ENTRY)
    try:
        with open(tmp_path, encoding="utf-8") as handle:
            if handle.read() != ENTRY:
                raise ValueError("read-back verification failed")
    finally:
        os.unlink(tmp_path)
    try:
        sys.stdout.write(ENTRY)
        sys.stdout.flush()
    except (BrokenPipeError, OSError):
        # Fall back to writing the entry to a file if stdout is unavailable.
        fallback = os.environ.get("MAKEFUN_OUTPUT") or "./output/entry.txt"
        parent = os.path.dirname(fallback)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(fallback, "w", encoding="utf-8") as handle:
            handle.write(ENTRY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
