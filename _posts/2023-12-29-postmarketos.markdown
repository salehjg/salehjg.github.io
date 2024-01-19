---
layout: post
title:  "PostMarketOS on Xiaomi Note 4X"
date:   2023-12-29 12:32:45 +0330
categories:
---
<img align="right" width="150" src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/PostmarketOS_logo.svg/2048px-PostmarketOS_logo.svg.png">

# PostMarketOS on Xiaomi Note 4X
PostMarketOS, an Alpine Linux based distro for smartphones, offers an amazing opportunity for the old Android phones with unlocked bootloaders to be used as portable Linux boxes.
I tried it on my old Xiaomi Note 4X (mido) with Snapdragon `aarch64` SoC, and it worked great out of the box. The sim card data along with some other peripherals are not working, but you do not really need them as the WiFi adapter is stable and working.

## Steps
```
sudo pacman -S pmbootstrap
pmbootstrap init # select v23.1??, not edge! in edge, wifi does not work
pmbootstrap install
pmbootstrap flasher flash_lk2nd
pmbootstrap flasher flash_rootfs

# To modify the kernel to support nfs and smb.
# See this link: https://gitlab.com/postmarketOS/pmaports/-/issues/956
pmbootstrap init
pmbootstrap kconfig edit linux-postmarketos-qcom-msm8953 # to enable NFS and SMBv3 support from file systems menu
pmbootstrap pkgrel_bump linux-postmarketos-qcom-msm8953 
pmbootstrap build --force --arch aarch64 linux-postmarketos-qcom-msm8953 # to build the kernel from the source
pmbootstrap build device-xiaomi-mido --force # to build the rest
pmbootstrap flasher flash_kernel
```
Before running flasher commands, you have to reboot your phone to custom recovery mode. After normal reboot and after the vibration, press and hold only the volume-down key (dont hold any other key, including power). Now connect the usb cable and run the flasher commands.

## Firewall

## SD Card

## Battery Life

## Samba Server
