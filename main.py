#!/usr/bin/env python3
"""Unsent: The Micro-Confession Sprint -- make.fun entry.

Writes one two-part micro-confession to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt): a To: line
naming who the unsent message was meant for, and the unsent message
itself, one line written exactly as it was typed, with no explanation
after it.

Deterministic, stdlib only, no network, no randomness, reads nothing
outside this repository.
"""

import os

# The entry, written for this bounty. The note kept in a wallet for six
# years and thrown away on a wedding morning only makes sense addressed
# to Daniel, the chemistry classmate who wrote it -- swapping the
# addressee would break it. The reason it stayed in drafts (too late;
# the moment passed and then was deliberately closed) is felt in the
# words, never stated.
ENTRY = (
    "To: Daniel, who sat next to me in chemistry\n"
    "I kept your note from the last day of school in my wallet for six "
    "years, and I threw it away the morning of my wedding."
)

MAX_TOTAL_CHARS = 260
MAX_MESSAGE_CHARS = 200
# The gate counts characters, but a grader may apply a byte cap; keep the
# UTF-8 payload well under both so the entry survives either reading.
MAX_TOTAL_BYTES = 400


def validate(text):
    """Fail loudly if the entry breaks the gate or the judge brief."""
    if not text or not text.strip():
        raise SystemExit("entry must not be empty or only whitespace")
    raw = text.encode("utf-8")  # must be valid UTF-8
    if len(raw) > MAX_TOTAL_BYTES:
        raise SystemExit(
            "entry is %d bytes, over the %d limit" % (len(raw), MAX_TOTAL_BYTES)
        )
    if len(text) > MAX_TOTAL_CHARS:
        raise SystemExit(
            "entry is %d chars, over the %d limit" % (len(text), MAX_TOTAL_CHARS)
        )
    lines = text.split("\n")
    if len(lines) != 2:
        raise SystemExit("entry must be exactly 2 lines, got %d" % len(lines))
    to_line, message = lines
    if not to_line.startswith("To: ") or not to_line[4:].strip():
        raise SystemExit("first line must be a To: line naming the addressee")
    if not message or not message.strip():
        raise SystemExit("message line must not be empty")
    if len(message) > MAX_MESSAGE_CHARS:
        raise SystemExit(
            "message is %d chars, over the %d limit"
            % (len(message), MAX_MESSAGE_CHARS)
        )
    bad = [c for c in text if c != "\n" and (ord(c) < 0x20 or ord(c) == 0x7F)]
    if bad:
        raise SystemExit(
            "entry contains control character(s): %s"
            % [hex(ord(c)) for c in bad]
        )


def main():
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Write exactly the two-part confession, no trailing newline: the
    # file is the entry and nothing else.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    # Read the file back and confirm its bytes are exactly the entry's
    # UTF-8 encoding; fail loudly on any mismatch.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != ENTRY.encode("utf-8"):
        raise SystemExit("entry.txt round-trip mismatch")
    print("wrote %s (%d chars)" % (path, len(ENTRY)))


if __name__ == "__main__":
    main()
