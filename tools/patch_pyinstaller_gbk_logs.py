#!/usr/bin/env python3
"""Replace non-GBK log glyphs in an embedded PyInstaller api_server module."""

from __future__ import annotations

import argparse
import shutil
import zlib
from pathlib import Path

from PyInstaller.archive.readers import CArchiveReader


REPLACEMENTS = {
    bytes.fromhex("f09f94a7"): b"TOOL",
    bytes.fromhex("e284b9efb88f"): b"[INFO]",
    bytes.fromhex("e29aa0efb88f"): b"[WARN]",
    bytes.fromhex("e29c85"): b"OK!",
}


def find_pyz_name(reader: CArchiveReader) -> str:
    names = [name for name, entry in reader.toc.items() if entry[4] == "z"]
    if len(names) != 1:
        raise RuntimeError(f"Expected one PYZ entry, found {names!r}")
    return names[0]


def patch_executable(source: Path, destination: Path) -> None:
    archive = CArchiveReader(str(source))
    pyz = archive.open_embedded_archive(find_pyz_name(archive))
    typecode, module_offset, compressed_length = pyz.toc["api_server"]

    raw = pyz.extract("api_server", raw=True)
    if raw is None:
        raise RuntimeError("api_server has no bytecode payload")

    patched = raw
    counts: dict[str, int] = {}
    for old, new in REPLACEMENTS.items():
        count = patched.count(old)
        if count == 0:
            raise RuntimeError(f"Pattern {old.hex()} was not found")
        counts[old.hex()] = count
        patched = patched.replace(old, new)

    candidates = [zlib.compress(patched, level) for level in range(1, 10)]
    candidates = [data for data in candidates if len(data) <= compressed_length]
    if not candidates:
        raise RuntimeError("Patched api_server does not fit in its original PYZ slot")

    compressed = min(candidates, key=len)
    padded = compressed + (b"\0" * (compressed_length - len(compressed)))

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    absolute_offset = pyz._start_offset + module_offset
    with destination.open("r+b") as handle:
        handle.seek(absolute_offset)
        handle.write(padded)

    verified_pyz = CArchiveReader(str(destination)).open_embedded_archive(find_pyz_name(CArchiveReader(str(destination))))
    verified = verified_pyz.extract("api_server", raw=True)
    if verified != patched:
        raise RuntimeError("Patched bytecode verification failed")
    if any(old in verified for old in REPLACEMENTS):
        raise RuntimeError("A non-GBK log pattern remains after verification")

    print(f"patched={destination}")
    print(f"slot={compressed_length}; payload={len(compressed)}; replacements={counts}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    patch_executable(args.source.resolve(), args.destination.resolve())


if __name__ == "__main__":
    main()
