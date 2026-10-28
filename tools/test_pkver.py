"""Tests for pkver. Run: python3 tools/test_pkver.py"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import pkver  # noqa: E402

BUMP_CASES = [
    ("7.2.11.arch1", "7.2.11.arch1.tol1"),
    ("7.2.11.arch1.tol1", "7.2.11.arch1.tol2"),
    ("7.2.11.arch1.tol2", "7.2.11.arch1.tol3"),
    ("6.17.4.arch1", "6.17.4.arch1.tol1"),
]

UNAME_CASES = [
    # (pkgver, pkgrel, expected)
    ("7.2.11.arch1", "1", "7.2.11-arch1-1-ilol"),
    ("7.2.11.arch1.tol1", "1", "7.2.11-arch1-1-ilol"),
    ("7.2.11.arch1.tol2", "1", "7.2.11-arch1-1-ilol"),
    ("6.17.4.arch1", "2", "6.17.4-arch1-2-ilol"),
]


def run() -> int:
    failed = 0
    for pkgver, want in BUMP_CASES:
        got = pkver.bump_tol(pkgver)
        if got != want:
            print(f"FAIL bump {pkgver}: {got}")
            failed += 1
        else:
            print(f"ok   bump {pkgver} -> {got}")

    for pkgver, rel, want in UNAME_CASES:
        got = pkver.uname_suffix(pkgver, rel)
        if got != want:
            print(f"FAIL uname {pkgver}: {got}")
            failed += 1
        else:
            print(f"ok   uname {pkgver} -> {got}")

    # .tolN must never leak into uname
    assert ".tol" not in pkver.uname_suffix("7.2.11.arch1.tol9")

    # garbage refuses loudly
    for bad in ("", "1.0", "7.2.11", "7.2.11.x", "bogus", "7.2.11.arch1-tol"):
        try:
            pkver.parse(bad)
            print(f"FAIL parse {bad!r}: should raise VersionError")
            failed += 1
        except pkver.VersionError:
            print(f"ok   rejects {bad!r}")

    # CLI round trip
    for args, expect in (
        (["bump", "7.2.11.arch1"], "7.2.11.arch1.tol1"),
        (["uname-suffix", "7.2.11.arch1.tol1"], "7.2.11-arch1-1-ilol"),
    ):
        out = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "pkver.py"), *args],
            capture_output=True, text=True,
        )
        if out.returncode != 0 or out.stdout.strip() != expect:
            print(f"FAIL cli {args}: rc={out.returncode} out={out.stdout!r}")
            failed += 1
        else:
            print(f"ok   cli {args[0]}")

    print(f"{len(BUMP_CASES)+len(UNAME_CASES)+9} checks, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(run())
