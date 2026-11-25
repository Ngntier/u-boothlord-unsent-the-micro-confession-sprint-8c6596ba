#!/usr/bin/env python3
"""Unsent: The Micro-Confession Sprint — make.fun entry
u-boothlord-unsent-the-micro-confession-sprint-8c6596ba.

Writes one micro-confession in exactly two parts to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt):
a To: line naming who it was meant for, and the unsent message
itself, one line written exactly as it was typed, with no
explanation after it.

Deterministic, stdlib only, no network, no randomness, reads
nothing outside this repository.
"""

import os

# The entry: one original micro-confession, written for this bounty.
# The To: line and the message need each other — the ritual (rehearsing
# on the Sunday drive home) only makes sense addressed to Mom, and the
# reason it stayed in drafts (fear of saying it out loud) is felt in
# the swerve to the garden, never stated.
ENTRY = (
    "To: Mom\n"
    "I rehearse telling you I quit my degree every Sunday on the drive "
    "home, and every Sunday I ask about your garden instead."
)

MAX_TOTAL_CHARS = 260
MAX_MESSAGE_CHARS = 200


def validate(text: str) -> None:
    """Fail loudly if the entry breaks the RULES.txt gate or the judge brief."""
    if not text or not text.strip():
        raise SystemExit("entry must not be empty or only whitespace")
    encoded = text.encode("utf-8")  # must be valid UTF-8
    if len(text) > MAX_TOTAL_CHARS:
        raise SystemExit(
            f"entry is {len(text)} chars, over the {MAX_TOTAL_CHARS} limit"
        )
    # Exactly two parts, separated by one newline: the To: line and the
    # message. No explanation after the message, no extra lines.
    lines = text.split("\n")
    if len(lines) != 2:
        raise SystemExit(f"entry must be exactly 2 lines, got {len(lines)}")
    to_line, message = lines
    if not to_line.startswith("To: ") or not to_line[4:].strip():
        raise SystemExit("first line must be a To: line naming the addressee")
    if not message or not message.strip():
        raise SystemExit("message line must not be empty")
    if len(message) > MAX_MESSAGE_CHARS:
        raise SystemExit(
            f"message is {len(message)} chars, over the {MAX_MESSAGE_CHARS} limit"
        )
    # No control characters anywhere except the single separating newline.
    bad = [c for c in text if c != "\n" and (ord(c) < 0x20 or ord(c) == 0x7F)]
    if bad:
        raise SystemExit(
            f"entry contains control character(s): {[hex(ord(c)) for c in bad]}"
        )


def main() -> None:
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Write exactly the two-part confession, no trailing newline: the
    # file is the entry and nothing else.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    # Write-verify round trip: read the file back and confirm its bytes
    # are exactly the entry's UTF-8 encoding.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != ENTRY.encode("utf-8"):
        raise SystemExit("entry.txt round-trip mismatch")
    print(f"wrote {path} ({len(ENTRY)} chars)")


if __name__ == "__main__":
    main()
