// SPDX-License-Identifier: GPL-2.0
//
// first-tol — a Rust-for-Linux out-of-tree module.
//
// `first-tol.c` proves linux-ilol-headers loads C modules. This proves the
// same for Rust: Arch's official kernel ships CONFIG_RUST=y (verified on
// 7.2.11.arch1-1), so linux-ilol keeps Rust available too.
//
// Build (needs the headers tree and the system rustc):
//     make -C samples/rust
//     insmod first-tol.ko && dmesg | tail
//
// Reference: Rust-for-Linux documentation,
// Documentation/rust/ in the kernel tree — examples from the mainline
// samples/rust directory.

use kernel::prelude::*;

module! {
    type: FirstTol,
    name: "first-tol-rs",
    author: "TOL — the ominous linux",
    description: "Rust header sanity check for linux-ilol",
    license: "GPL",
}

struct FirstTol;

impl kernel::Module for FirstTol {
    fn init(_module: &'static ThisModule) -> Result<Self> {
        pr_info!("first-tol-rs: Rust modules load against linux-ilol headers\n");
        Ok(FirstTol)
    }
}

impl Drop for FirstTol {
    fn drop(&mut self) {
        pr_info!("first-tol-rs: goodbye\n");
    }
}
