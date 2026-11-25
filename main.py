#!/usr/bin/env python3
"""One Line, One Laugh - make.fun entry.

The program writes exactly one funny line of at most 140 characters
to $MAKEFUN_OUTPUT_DIR/entry.txt. The line is a constant in this file,
so every run produces the same output. Stdlib only, deterministic,
no network.
"""
import os
import sys

ENTRY = 'I told my therapist I fear commitment, so I ghosted my own wedding. Twice.'
MAX_CHARS = 140


def validate(text):
    """Check a candidate line against the one-line, 140-char gates."""
    if not text or not text.strip():
        raise ValueError("entry is empty or whitespace-only")
    # The file holds the line plus one trailing newline, so the gate
    # counts that extra byte as well.
    if len(text) + 1 > MAX_CHARS:
        raise ValueError(
            "entry file would be %d chars, over the %d-char gate"
            % (len(text) + 1, MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def validate_written(path):
    """Read entry.txt back from disk and re-check the artifact itself.

    Validating the file on disk (rather than only the in-memory string)
    catches encoding or write errors that would otherwise ship
    silently: the artifact is what gets graded, not the constant.
    """
    with open(path, "rb") as f:
        raw = f.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("entry.txt is not valid UTF-8: %s" % exc)
    validate(text.rstrip("\n"))
    if text.count("\n") > 1:
        raise ValueError("entry.txt must be a single line")
    return text


def write_entry():
    """Write the validated line to entry.txt and confirm the round trip."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    target = os.path.join(out_dir, "entry.txt")
    os.makedirs(out_dir, exist_ok=True)
    data = (validate(ENTRY) + "\n").encode("utf-8")
    with open(target, "wb") as f:
        f.write(data)
    with open(target, "rb") as f:
        if f.read() != data:
            raise ValueError("entry.txt round-trip mismatch")
    validate_written(target)
    return target


def main(argv):
    if "--self-test" in argv:
        validate(ENTRY)
        print("self-test ok: %d chars" % len(ENTRY))
        return 0
    if "--check" in argv:
        validate(ENTRY)
        print("check ok: %d chars, within %d" % (len(ENTRY), MAX_CHARS))
        return 0
    try:
        write_entry()
    except ValueError as exc:
        print("invalid entry: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
