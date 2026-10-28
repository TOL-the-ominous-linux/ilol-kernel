# Makefile for the first-tol module — build with the running kernel's
# headers (or KDIR=<...> to target another tree, e.g. linux-ilol-headers).
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
