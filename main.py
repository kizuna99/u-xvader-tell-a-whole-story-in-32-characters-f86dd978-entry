# SPDX-License-Identifier: MIT
"""Tell a Whole Story in 32 Characters — writes the Wi-Fi name to /output/entry.txt."""
import os

# The winning line: 31 characters, pure ASCII. "finally" carries the whole
# backstory — a dad who left for milk years ago has, at last, come back —
# so the twist lands on the first read and every character earns its place.
LINE = "Dad finally came back with milk"


def main() -> None:
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "entry.txt")
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(LINE)
    except OSError:
        fallback = os.path.join(os.getcwd(), "output")
        os.makedirs(fallback, exist_ok=True)
        with open(os.path.join(fallback, "entry.txt"), "w", encoding="utf-8", newline="") as fh:
            fh.write(LINE)


if __name__ == "__main__":
    main()
