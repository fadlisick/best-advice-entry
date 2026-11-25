#!/usr/bin/env python3
"""The Best Advice I Ever Got — make.fun program/v1 entry.

Writes one sentence — the best advice the writer ever received — to
/output/entry.txt, then verifies the file byte-for-byte against the
locked line. Deterministic: the same bytes on every run.
"""

import os

ADVICE = (
    "My driving instructor told me in a snowstorm to look where I wanted "
    "the car to go instead of staring at the ditch I was trying to miss."
)

MIN_CHARS = 1
MAX_CHARS = 200


def output_folder():
    """Where the harness collects the entry (MAKEFUN_OUTPUT_DIR or /output)."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def write_entry():
    os.umask(0o022)
    folder = output_folder()
    os.makedirs(folder, exist_ok=True)
    target = os.path.join(folder, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(ADVICE)
    os.chmod(target, 0o644)
    return target


def verify_entry():
    """Re-read entry.txt and check it against the gate, byte for byte."""
    target = os.path.join(output_folder(), "entry.txt")
    with open(target, "rb") as handle:
        raw = handle.read()
    text = raw.decode("utf-8")
    if len(raw) != len(ADVICE.encode("utf-8")):
        raise SystemExit("gate: entry byte length changed")
    if text != ADVICE:
        raise SystemExit("entry.txt does not match the locked line")
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise SystemExit("gate: entry must be 1-200 characters")
    if "\n" in text or "\r" in text:
        raise SystemExit("gate: entry must be a single line")
    if text != text.strip():
        raise SystemExit("gate: no leading or trailing whitespace")
    if not text.endswith("."):
        raise SystemExit("gate: entry must be one complete sentence")
    if "—" in text:
        raise SystemExit("gate: no em dash allowed")
    return text


if __name__ == "__main__":
    write_entry()
    checked = verify_entry()
    print("entry.txt OK: %d chars" % len(checked))
