#!/usr/bin/env python3
"""pkver — iLOL kernel version naming, usable as library or CLI.

Two naming layers, kept in one place so the PKGBUILD and release notes
cannot drift apart:

  pkgver     6.17.4.arch1-1        Arch
             6.17.4.arch1-1.tol1   first TOL build, .tolN bumps per change
  uname -r   7.2.11-arch1-1-ilol   LOCALVERSION suffix, no .tolN — the
                                    kernel build is the pkgver's job

See POLICY.md § Versioning. A rebuild that changes nothing gets no new
.tolN; this module is the single place both strings are minted and read.
"""

from __future__ import annotations

import argparse
import json
import re
import sys

ARCH_RE = re.compile(
    r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"
    r"\.arch1-(?P<rel>\d+)(?P<tol>\.tol\d+)?$"
)

LOCALVERSION = "-ilol"


class VersionError(ValueError):
    """Not a version string this package can carry."""


def parse(pkgver: str) -> dict[str, str]:
    """Parse an Arch or TOL pkgver into its fields. Raises VersionError."""
    m = ARCH_RE.match(pkgver)
    if not m:
        raise VersionError(
            f"not an arch1-style pkgver (optionally +.tolN): {pkgver!r}"
        )
    return {
        "major": m["major"],
        "minor": m["minor"],
        "patch": m["patch"],
        "rel": m["rel"],
        "tol": m["tol"].lstrip(".") if m["tol"] else "",
    }


def bump_tol(pkgver: str) -> str:
    """Return pkgver with the .tolN revision advanced by one."""
    v = parse(pkgver)
    next_n = int(v["tol"][3:]) + 1 if v["tol"] else 1
    base = f"{v['major']}.{v['minor']}.{v['patch']}.arch1-{v['rel']}"
    return f"{base}.tol{next_n}"


def uname_suffix(pkgver: str) -> str:
    """The `uname -r` suffix: the arch part, then the fixed -ilol mark.

    The .tolN packaging revision does NOT appear in uname -r: two rebuilds
    that only change packaging report the same kernel identity on purpose,
    while the packages differ. See POLICY.md.
    """
    v = parse(pkgver)
    return f"-arch1-{v['rel']}{LOCALVERSION}"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true", help="output JSON")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, help_ in (
        ("parse", "print the pkgver fields"),
        ("bump", "advance the .tolN revision by one"),
        ("uname-suffix", "print the `uname -r` suffix"),
    ):
        p = sub.add_parser(name, help=help_)
        p.add_argument("pkgver")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "bump":
            out: str | dict = bump_tol(args.pkgver)
        elif args.cmd == "parse":
            out = parse(args.pkgver)
        else:
            out = uname_suffix(args.pkgver)
    except VersionError as e:
        print(f"pkver: {e}", file=sys.stderr)
        return 1
    print(json.dumps(out) if args.json else out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
