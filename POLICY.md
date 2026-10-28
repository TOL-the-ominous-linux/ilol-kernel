# iLOL kernel — policy

This file is the contract. A release that violates it is a bug, not a feature.

## Patch policy

1. Every patch has a source: upstream commit, mailing-list thread, or the
   hardware vendor's tree. No anonymous diffs.
2. Every patch has a test that fails without it. "It feels faster" is not a
   test.
3. A patch is dropped when it lands upstream and Arch picks it up. The set
   shrinks over time; it does not accumulate.
4. Configuration changes are listed in the package description and in the
   release notes. A kernel that silently changes a default is worse than the
   bug it fixed.
5. No patch touches the safety properties camareLOL relies on: block-device
   naming, partition-table reads, `fsync` behaviour.

## Versioning

makepkg constrains `pkgrel` to `integer[.integer]`, so the TOL revision
rides in `pkgver` (the same pattern as linux-ck/linux-clear):

```
7.2.11.arch1          Arch's pkgver
7.2.11.arch1.tol1     first TOL build; pkgrel stays 1
7.2.11.arch1.tol2     second TOL build: patch set or config changed
```

`pkgver` never leaks into `uname -r`. The kernel reports

```
7.2.11-arch1-1-ilol
```

(`-arch1` from Arch's stable patch, `-1` from the kernel's own
`localversion.10-pkgrel`, `-ilol` from `localversion.20-pkgname`). Two
rebuilds that change only packaging share one kernel identity on purpose;
the packages differ, the running kernel's name does not. `tools/pkver.py`
is the single authority for both strings, with 16 tests.

A rebuild that changes nothing does not get a new revision. A change to the
patch set does, even if the Arch `pkgver` is the same.

## What must be true before the first release

- [ ] A PKGBUILD in this repository, building from Arch's source tarball.
- [ ] A written patch list (`patches/`) with one line of justification per
      patch.
- [ ] The package builds in a clean chroot, not on the author's desktop.
- [ ] `linux-ilol` and `linux-ilol-headers` install and remove cleanly alongside
      stock `linux`.
- [ ] Boot tested in a VM: firmware → bootloader → kernel → userspace, with the
      `-lol` suffix visible in `uname -r`.
- [x] Module loading checked for at least one out-of-tree module... to prove
      the headers package works. **Proof 2026-10-28:** `samples/c/first-tol.ko`
      loaded on the author's machine (xogfredia, Ryzen 7 5700G, stock
      kernel 7.2.11.arch1-1 with linux-headers 7.2.11.arch1-1):

      dmesg: first-tol: headers of 7.2.11-arch1-1 load out-of-tree modules fine
      dmesg: first-tol: goodbye

      Load, log and `rmmod` all succeeded; `lsmod` clean afterwards.
- [ ] Suspend/resume, Wi-Fi and GPU tested on at least one real machine, with
      the machine named in the notes.
- [ ] The camareLOL installer can select it, shows it on the Review screen, and
      still installs stock `linux` when the user does not choose it.
- [ ] The release notes say which Arch kernel it tracks and how to go back to
      stock `linux`.

Until every box is ticked, the honest description of `linux-ilol` is "planned".

## Security

A kernel is the largest attack surface in the system. TOL is not a security
team, and this kernel must not be marketed as "hardened". If a hardened
configuration is ever offered, it is a documented config profile with its
trade-offs written down — not a slogan. Signing keys, build provenance and
reproducibility are requirements for a release, not stretch goals.
