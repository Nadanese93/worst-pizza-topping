#!/usr/bin/env python3
"""The Worst Pizza Topping - sandpaper one-liner.

Prints the entry to stdout and writes it byte-identical to
$MAKEFUN_OUTPUT_DIR/entry.txt (or ./entry.txt when the env var is unset).
"""

import hashlib
import os
import sys

ENTRY = "Try our sandpaper pizza: it exfoliates your tongue, files your teeth down to a shine, and the crust comes with a safety warning."

EXPECTED_SHA256 = "31f8ab2b7b592a462b67e6bd4d95a9f4b13bc166a8f73bd9fb77f21aaaab4fe4"


def verify(path: str) -> int:
    """Read the written entry back from disk and check it against the gate.

    Returns 0 when every check passes, 1 otherwise (with an error on stderr).
    """
    try:
        with open(path, "rb") as f:
            raw = f.read()
    except OSError as exc:
        print(f"verify: cannot read {path}: {exc}", file=sys.stderr)
        return 1
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        print("verify: entry is not valid UTF-8", file=sys.stderr)
        return 1
    if not 1 <= len(text) <= 200:
        print(f"verify: length {len(text)} outside 1-200 characters", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("verify: entry must be a single line with no newline", file=sys.stderr)
        return 1
    bad = [c for c in text if ord(c) < 0x20]
    if bad:
        print(f"verify: control character U+{ord(bad[0]):04X} found", file=sys.stderr)
        return 1
    if hashlib.sha256(raw).hexdigest() != EXPECTED_SHA256:
        print("verify: sha256 mismatch against canonical entry", file=sys.stderr)
        return 1
    return 0


def main() -> int:
    data = ENTRY.encode("utf-8")
    os.write(1, data)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(data)
    return verify(path)


if __name__ == "__main__":
    raise SystemExit(main())
