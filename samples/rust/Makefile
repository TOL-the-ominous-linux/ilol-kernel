# Makefile for the Rust out-of-tree sample module.
# Requires a kernel tree with CONFIG_RUST=y (Arch's official kernel ships
# it enabled; linux-ilol must too) and the system rustc.
obj-m := first-tol.o

RUST_SHADOW ?=  # build crate sources first when added beyond first-tol.rs

first-tol-objs := rust/target.o

KDIR ?= /lib/modules/$(shell uname -r)/build
PWD  := $(shell pwd)

all: first-tol.ko

first-tol.ko:
	$(MAKE) -C $(KDIR) M=$(PWD) RUST_ORIGINAL_CLIPPY_ARGS= modules

install: first-tol.ko
	$(MAKE) -C $(KDIR) M=$(PWD) modules_install

clean:
	$(MAKE) -C $(KDIR) M=$(PWD) clean

.PHONY: all install clean
