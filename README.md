# iLOL kernel

**Status: planned. Nothing is built, packaged or shipped yet.**

The kernel line of [The Ominous Linux](https://github.com/TOL-the-ominous-linux/.github) —
the packages that [camareLOL](https://github.com/TOL-the-ominous-linux/camareLOL)
may install when the stock Arch kernel is not enough for a machine.

Examples before versions exist so that mistakes get made *before* an upstream
kernel has to carry them.

## Where the code lives

| Directory | Content |
|---|---|
| [`patches/`](patches/) | the patch set — every diff has a source, a test and one line of justification |
| [`tools/`](tools/) | Python packaging helpers (version naming is the first one) — userspace only |
| [`samples/`](samples/) | out-of-tree build proofs: a C module and a Rust module, and why there is no C++ one |

The kernel itself is C — that is what the Linux kernel is — with Rust as the
upstream-supported second language (`CONFIG_RUST=y` ships enabled in Arch's
official kernel, verified on 7.2.11.arch1-1). Python runs the packaging
tooling. Sample modules are how the header package is proven alive before
the first release.

## What it is

`iLOL kernel` is **Arch-based**: it tracks Arch's `linux` package, keeps Arch's
configuration and patch set, and adds a small, documented set of changes. It is
delivered as normal Arch packages:

| Package | Provides |
|---|---|
| `linux-ilol` | the kernel image, modules and firmware hooks |
| `linux-ilol-headers` | headers for out-of-tree modules |

`uname -r` must show the suffix, so a support request can tell which kernel is
running: `6.x.y-arch1-1-ilol`.

## What it is not

- **Not a distribution.** camareLOL installs Arch Linux. This is a package
  choice inside that install, not a separate OS.
- **Not a fork with its own subsystem.** TOL does not maintain a Linux fork.
  Patches come from upstream, from Arch, or from a named source with a link.
- **Not the default.** Stock `linux` stays the default. `linux-ilol` is opt-in,
  chosen explicitly, and the installer must say so on the Review screen.
- **Not a performance meme.** No "gaming" sysctl bundles, no scheduler swaps
  without a measured reason, no patch that only exists to make a benchmark
  number move.

## Why it might exist

A separate line is justified only for hardware that is known to be painful on a
fresh Arch install — for example machines whose Wi-Fi or touchpad needs a patch
that has not reached the stable Arch package yet, or where a specific documented
module option is needed. Each case needs a machine, a symptom, a patch and a
test. A wishlist is not a reason to ship a kernel.

## Full policy

[POLICY.md](POLICY.md) is the contract: patch rules, versioning, and the
checklist every box of which must be ticked before the first release. Until
then the honest description of `linux-ilol` is **"planned"**.

```
patches/         empty by design, see POLICY.md — an anonymous diff is a bug
```

## Relationship to camareLOL

camareLOL does not need the iLOL kernel to work. If it is ever offered in the
installer it must be **off by default**, **named on the Review screen**,
**reversible** (the notes state the command that restores stock `linux`), and
**tested by the same acceptance harness** as the rest of the install. If those
four conditions cannot be met, the kernel line stays outside camareLOL as a
package people install themselves.

## Links

- Main project: <https://github.com/TOL-the-ominous-linux/camareLOL>
- Organisation: <https://github.com/TOL-the-ominous-linux/.github>
- Why the name: [camareLOL branding](https://github.com/TOL-the-ominous-linux/.github#readme)

---

*The Ominous Linux logo and mark are inspired by the band TOOL. The Ominous
Linux is not affiliated with, endorsed by, or connected to the band.*
