# tools/ — packaging helpers (Python)

Small userspace scripts the PKGBUILD and release flow call. They run on the
packaging host, never inside the kernel.

| Script | What it does | Test |
|---|---|---|
| [`pkver.py`](pkver.py) | mints/reads the `.tolN` packaging revision and the `-ilol` `uname -r` suffix — the single naming authority per POLICY.md § Versioning | [`test_pkver.py`](test_pkver.py) — 11 checks, exits non-zero on failure |

Run the tests before touching anything else here:

```console
$ python3 tools/test_pkver.py
11 checks, 0 failed
```
