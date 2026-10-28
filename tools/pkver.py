#!/usr/bin/env python3
"""pkver — iLOL kernel version naming, usable as library or CLI.

Two naming layers, kept in one place so the PKGBUILD and release notes
cannot drift apart:

  pkgver     7.2.11.arch1          Arch's own pkgver line
             7.2.11.arch1.tol1     first TOL build; .tolN bumps per change
  pkgrel     1                     always 1 — the revision lives in pkgver
  uname -r   7.2.11-arch1-1-ilol   fixed localversion mark, no .tolN

makepkg constrains pkgrel to integer[.integer], which is why the .tolN
revision rides in pkgver (the pattern linux-ck/linux-clear use), not in
pkgrel. The .tolN never reaches uname -r on purpose: two rebuilds that
only change packaging report the same kernel identity while the packages
differ. See POLICY.md § Versioning.
"""

from __future__ import annotations

import argparse
import json
import re
import sys

PKGVER_RE = re.compile(
    r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"
    r"\.(?P<kernelid>arch\d+)"
    r"(?P<tol>\.tol\d+)?(?P<rel>-(?P<relnum>\d+))?$"
)

# The pkgbase and localversion constants in one place.
PKGBASE = "linux-ilol"
LOCALVERSION = "-ilol"
LOCALVERSION_FILE = "localversion.20-pkgname"


class VersionError(ValueError):
    """Not a version string this package can carry."""


def parse(pkgver: str) -> dict[str, str]:
    """Parse an Arch or TOL pkgver (pkgver line, no pkgrel) into fields."""
    m = PKGVER_RE.match(pkgver)
    if not m:
        raise VersionError(
            f"not an arch-style pkgver (optionally .tolN / -rel): {pkgver!r}"
        )
    return {
        "major": m["major"],
        "minor": m["minor"],
        "patch": m["patch"],
        "kernelid": m["kernelid"],
        "tol": m["tol"].lstrip(".") if m["tol"] else "",
        "rel": m.group("relnum") or "",
    }


def bump_tol(pkgver: str) -> str:
    """Return pkgver with the .tolN revision advanced by one."""
    v = parse(pkgver)
    next_n = int(v["tol"][3:]) + 1 if v["tol"] else 1
    base = (f"{v['major']}.{v['minor']}.{v['patch']}.{v['kernelid']}")
    return f"{base}.tol{next_n}"


def uname_suffix(pkgver: str, pkgrel: str = "1") -> str:
    """The full version `uname -r` must show: `7.2.11-arch1-1-ilol`.

    The .tolN packaging revision does NOT appear in uname -r: two rebuilds
    that only change packaging report the same kernel identity on purpose.
    """
    v = parse(pkgver)
    rel = v["rel"] or pkgrel
    return (
        f"{v['major']}.{v['minor']}.{v['patch']}"
        f"-{v['kernelid']}-{rel}{LOCALVERSION}"
    )


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
        p.add_argument("--rel", default="1", help="pkgrel, default 1")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "bump":
            out: str | dict = bump_tol(args.pkgver)
        elif args.cmd == "parse":
            out = parse(args.pkgver)
        else:
            out = uname_suffix(args.pkgver, args.rel)
    except VersionError as e:
        print(f"pkver: {e}", file=sys.stderr)
        return 1
    print(json.dumps(out) if args.json else out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
