# Makefile for the Rust out-of-tree sample module.
# Requires a kernel tree with CONFIG_RUST=y (Arch's official kernel ships
# it enabled) and the system rustc. The kernel's Kbuild pattern rule
# compiles first-tol.rs -> first-tol.o directly; no extra targets.
obj-m := first-tol.o

KDIR ?= /lib/modules/$(shell uname -r)/build
PWD  := $(shell pwd)

all: first-tol.ko

first-tol.ko:
	$(MAKE) -C $(KDIR) M=$(PWD) modules

install: first-tol.ko
	$(MAKE) -C $(KDIR) M=$(PWD) modules_install

clean:
	$(MAKE) -C $(KDIR) M=$(PWD) clean

.PHONY: all install clean
