"""Tests for pkver. Run: python3 tools/test_pkver.py"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import pkver  # noqa: E402

CASES = [
    # (pkgver, expected bump, expected uname-suffix)
    ("6.17.4.arch1-1", "6.17.4.arch1-1.tol1", "-arch1-1-ilol"),
    ("6.17.4.arch1-1.tol1", "6.17.4.arch1-1.tol2", "-arch1-1-ilol"),
    ("7.2.11.arch1-1", "7.2.11.arch1-1.tol1", "-arch1-1-ilol"),
    ("7.2.11.arch1-1.tol2", "7.2.11.arch1-1.tol3", "-arch1-1-ilol"),
]


def run() -> int:
    failed = 0
    for pkgver, want_bump, want_uname in CASES:
        fields = pkver.parse(pkgver)
        assert fields["major"] == str(pkgver.split(".")[0])
        got_bump = pkver.bump_tol(pkgver)
        got_uname = pkver.uname_suffix(pkgver)
        if got_bump != want_bump or got_uname != want_uname:
            print(f"FAIL {pkgver}: bump={got_bump} uname={got_uname}")
            failed += 1
        else:
            print(f"ok   {pkgver} -> {got_bump} / {got_uname}")

    # .tolN must never leak into uname
    assert "-ilol" in pkver.uname_suffix("6.17.4.arch1-1.tol9")
    assert ".tol" not in pkver.uname_suffix("6.17.4.arch1-1.tol9")

    # garbage refuses loudly
    for bad in ("1.0.0", "7.2.11.arch1-1-x", "live-and-untested", ""):
        try:
            pkver.parse(bad)
            print(f"FAIL {bad!r}: should raise VersionError")
            failed += 1
        except pkver.VersionError:
            print(f"ok   rejects {bad!r}")

    # CLI round trip
    out = subprocess.run(
        [sys.executable, str(Path(__file__).parent / "pkver.py"),
         "bump", "7.2.11.arch1-1"],
        capture_output=True, text=True,
    )
    if out.returncode != 0 or out.stdout.strip() != "7.2.11.arch1-1.tol1":
        print(f"FAIL cli: rc={out.returncode} out={out.stdout!r} {out.stderr!r}")
        failed += 1
    else:
        print("ok   cli bump")

    print(f"{len(CASES)+7} checks, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(run())
