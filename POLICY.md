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

`pkgver` follows Arch's kernel package, plus a TOL revision:

```
6.17.4.arch1-1        Arch
6.17.4.arch1-1.tol1   first TOL build of that Arch kernel
6.17.4.arch1-1.tol2   second TOL build: patch set or config changed
```

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
- [ ] Module loading checked for at least one out-of-tree module (e.g. a
      filesystem or a network driver) to prove the headers package works.
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
