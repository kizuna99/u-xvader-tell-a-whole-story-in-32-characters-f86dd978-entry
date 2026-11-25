# SPDX-License-Identifier: MIT
"""Emit one Wi-Fi network name that tells a whole story in 32 characters.

The name is written, byte for byte and with no trailing newline, to
/output/entry.txt (override the directory with the OUTPUT_DIR env var).
The competition gate accepts UTF-8 text of 1 to 32 characters that is
not only whitespace, so the text is validated against those limits
before anything touches disk.
"""

import os
import sys
from pathlib import Path

# The story itself: a dad, an errand, and the years hidden in "finally".
STORY_TEXT = "Dad finally came back with milk"

# Gate limits from the competition rules.
MIN_CHARS = 1
MAX_CHARS = 32

OUTPUT_FILENAME = "entry.txt"


def build_payload() -> bytes:
    """Return the exact bytes to write, after checking the gate limits."""
    char_count = len(STORY_TEXT)
    if not MIN_CHARS <= char_count <= MAX_CHARS:
        raise ValueError(
            f"story is {char_count} characters; gate allows {MIN_CHARS}-{MAX_CHARS}"
        )
    if not STORY_TEXT.strip():
        raise ValueError("story must not be only whitespace")
    return STORY_TEXT.encode("utf-8")


def output_path() -> Path:
    directory = Path(os.environ.get("OUTPUT_DIR", "/output"))
    return directory / OUTPUT_FILENAME


def verify_round_trip(target: Path, expected: bytes) -> None:
    """Read the written file back and assert it matches what was intended.

    Guards against partial writes or encoding surprises: the bytes on
    disk must equal the payload exactly, and the decoded text must
    still satisfy the gate (1-32 characters, not only whitespace).
    """
    on_disk = target.read_bytes()
    if on_disk != expected:
        raise AssertionError(
            f"round-trip mismatch: wrote {len(expected)} bytes, "
            f"read back {len(on_disk)}"
        )
    decoded = on_disk.decode("utf-8")
    if not MIN_CHARS <= len(decoded) <= MAX_CHARS or not decoded.strip():
        raise AssertionError(f"round-trip text fails the gate: {decoded!r}")


def main() -> int:
    payload = build_payload()
    target = output_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(payload)
    verify_round_trip(target, payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
