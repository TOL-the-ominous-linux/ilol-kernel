# samples/ — live proofs, not demos

Each sample is one checklist item in [POLICY.md](../POLICY.md) turned into
something you can build and load. If it cannot build, it is a bug report.

| Directory | Language | Proves |
|---|---|---|
| [`c/`](c/) | C | `linux-ilol-headers` loads an out-of-tree C module |
| [`rust/`](rust/) | Rust | `linux-ilol` keeps `CONFIG_RUST=y` and loads out-of-tree Rust modules — Arch's official kernel ships Rust support enabled (verified on 7.2.11.arch1-1) |

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
