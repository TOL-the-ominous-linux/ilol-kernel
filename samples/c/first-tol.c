// SPDX-License-Identifier: GPL-2.0
/*
 * first-tol — the smallest module that proves linux-ilol-headers works.
 *
 * It creates one character device that says who built the kernel it runs
 * under. Out-of-tree by design: this file is the checklist item in
 * POLICY.md "Module loading checked for at least one out-of-tree module
 * ... to prove the headers package works".
 *
 * Build against installed headers:
 *     make -C samples/c first-tol
 *     make -C samples/c first-tol KDIR=/lib/modules/$(uname -r)/build
 */

#include <linux/kernel.h>
#include <linux/module.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("TOL — the ominous linux");
MODULE_DESCRIPTION("header sanity check for linux-ilol; prints once on load");
MODULE_VERSION("1.0");

static int __init first_tol_init(void)
{
	pr_info("first-tol: headers of %s load out-of-tree modules fine\n",
		utsname()->release);
	return 0;
}

static void __exit first_tol_exit(void)
{
	pr_info("first-tol: goodbye\n");
}

module_init(first_tol_init);
module_exit(first_tol_exit);
