#!/usr/bin/env python3
"""One line, one laugh: commitment issues, taken to their conclusion.

The entry is a single joke line — a therapy confession about fearing
commitment, escalated to ghosting one's own wedding, twice. The script
below keeps the joke inside the competition's 140-character, one-line
limit and delivers it as entry.txt.

Run it three ways:
    python3 main.py              write entry.txt
    python3 main.py --check      only validate, write nothing
    python3 main.py --self-test  validate, write, then re-read the file
                                 and confirm it is byte-for-byte right

MAKEFUN_OUTPUT_DIR picks the output folder (current directory if the
variable is missing). The script is deterministic, uses only the
standard library, and never touches the network.
"""

from pathlib import Path
import os
import sys

ENTRY = "I told my therapist I fear commitment, so I ghosted my own wedding. Twice."

LIMIT_CHARS = 140
FILE_NAME = "entry.txt"


class EntryError(Exception):
    """Raised when the entry or its written form breaks a rule."""


def guard(text):
    """Raise EntryError naming the first broken rule, if any.

    The length limit is checked first because it is the rule most likely
    to break when the joke is edited; the shape rules follow.
    """
    if not text:
        raise EntryError("entry is empty")
    if len(text) > LIMIT_CHARS:
        raise EntryError(
            "entry is %d characters, the limit is %d"
            % (len(text), LIMIT_CHARS)
        )
    if "\r" in text:
        raise EntryError("entry contains a carriage return")
    if text.count("\n") != 0:
        raise EntryError("entry must be a single line with no newline inside")


def target_file():
    """Return the entry.txt path, creating the output folder as needed."""
    folder = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or ".")
    folder.mkdir(parents=True, exist_ok=True)
    return folder / FILE_NAME


def persist():
    """Write the entry and verify the artifact by reading it back."""
    guard(ENTRY)
    path = target_file()
    encoded = (ENTRY + "\n").encode("utf-8")
    path.write_bytes(encoded)
    if path.read_bytes() != encoded:
        raise EntryError("entry.txt on disk does not match the entry")
    decoded = path.read_text(encoding="utf-8")
    if decoded != ENTRY + "\n":
        raise EntryError("entry.txt decoded to different text")
    guard(decoded[:-1])
    print("wrote %s (%d bytes)" % (path, len(encoded)))


def main(argv):
    try:
        if "--check" in argv:
            guard(ENTRY)
            print("check ok: one line, %d characters" % len(ENTRY))
        elif "--self-test" in argv:
            persist()
            print("self-test ok")
        elif len(argv) == 1:
            persist()
        else:
            raise EntryError("unrecognised arguments: %s" % " ".join(argv[1:]))
    except EntryError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
