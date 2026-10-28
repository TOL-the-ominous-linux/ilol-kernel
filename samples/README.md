# samples/ — live proofs, not demos

Each sample is one checklist item in [POLICY.md](../POLICY.md) turned into
something you can build and load. If it cannot build, it is a bug report.

| Directory | Language | Proves |
|---|---|---|
| [`c/`](c/) | C | `linux-ilol-headers` loads an out-of-tree C module — **proven on real hardware, see POLICY.md** |
| [`rust/`](rust/) | Rust | `linux-ilol` keeps `CONFIG_RUST=y` (verified on 7.2.11.arch1-1) |

## Why there is no C++ sample

Not a gap: C++ does not work in the Linux kernel. The kernel runtime has no
exceptions, no RTTI and no C++ standard-library allocator; mainline drivers
are written in C, with Rust as the only second supported language
(merged upstream in 6.1, documented in `Documentation/rust/`). A C++ sample
that "compiles" would not link against a real kernel, so adding one would
teach a lie. The languages that exist here are the languages that exist in
the kernel: C first, Rust second, and Python for the tooling in
[`tools/`](../tools/) — which runs in userspace during packaging, not
inside the kernel.

## Known limitation: out-of-tree Rust modules do not link today

The Rust sample **does not build against installed Arch headers** (tried
2026-10-28, rustc 1.99.1 / bindgen 0.73.2, both the exact versions the
kernel was built with):

```
error[E0514]: found crate `kernel` compiled by an incompatible version of rustc
```

rustc reports `libkernel.rmeta` (precompiled with the kernel in-tree) as
metadata-incompatible with an out-of-tree invocation, even though the
compiler version and commit hash are identical. The metadata check covers
more than the version string: the unstable build flags (`-Z` options,
sysroot, target spec) recorded when the kernel tree itself compiled its
Rust support crates do not match what an out-of-tree `make M=` run
produces. Upstream treats out-of-tree Rust modules as unfinished work in
progress.

Consequence for iLOL, written down so nobody rediscovers this the hard
way:

- The `CONFIG_RUST=y` claim stands — it is a build-time fact of Arch's
  kernel, checked in `/proc/config.gz`.
- What does not follow from that is "Rust modules can be built outside
  the kernel tree". Until upstream lands object-metadata compatibility,
  **Rust support is verified by building the kernel from source with an
  in-tree sample, not by loading an out-of-tree module.** That check
  belongs to the PKGBUILD step, not to a header-package proof.
- The sample stays in the tree as the target the build must reach — and
  as the first thing to re-run when upstream fixes it.
