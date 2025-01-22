---
layout: post
title:  "Setting up QEMU for RISCV64 on Archlinux"
date:   2025-01-22 12:32:45 +0330
categories: qemu
---
# Setting up QEMU for RISCV64 on Archlinux
```
sudo pacman -S qemu-user-binfmt
sudo pacman -S qemu-system-riscv # only if you need it
sudo systemctl restart systemd-binfmt
```

Having `qemu-user-binfmt`, you can run binaries built for RISCV64 on your AMD64 machine. 
This is essential for cross-compiling non-flexable projects for RISCV64 such as GCC.
