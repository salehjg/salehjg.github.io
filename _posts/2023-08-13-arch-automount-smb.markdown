---
layout: post
title:  "Automount for Raspberry PI SMB Server"
date:   2023-08-13 12:32:45 +0330
categories:
---

# Automount for Raspberry Pi SMB Server
I use Archlinux and have a RPi3 that runs a Samba server as my homebew NAS. 
To automatically mount the NAS drive when accessed, one could use automount as described below:

## Step 1
```bash
sudo pacman -S smbclient
sudo mkdir /mnt/rpi3
sudo chown $(whoami) /mnt/rpi3
```

## Step 2
Run `sudo nano /etc/systemd/system/mnt-rpi3.mount` and save the following content in it. Before you save it, replace:
- User name (`saleh` with your user's name)
- IP (`192.168.100.111` with your server's IP)
- Make sure the share point name is set to `rpi3`, otherwise the mount point's directory should also be renamed along with `rpi3` occurrences in `*.mount` and `*.automount` of Step 3.
- Replace `YOUR_NAS_USER` and `YOUR_PASSWORD` with your NAS's register username and password (not a good idea to authenticate this way!!).

```
[Unit]
  Description=rpi3 smb mounter
  Requires=network-online.target
  After=network-online.service
[Mount]
  What=//192.168.100.111/rpi3
  Where=/mnt/rpi3
  Options=uid=saleh,username=YOUR_NAS_USER,password=YOUR_PASSWORD
  Type=cifs
[Install]
  WantedBy=multi-user.target
```

## Step 3
Run `sudo nano /etc/systemd/system/mnt-rpi3.automount` and save the following content in it:
- Timeout is in seconds, set to `0` to disable it. 
- Rename `rpi3` with your sharepoint's name.

```
[Unit]
Description=Automount rpi3
[Automount]
Where=/mnt/rpi3/
TimeoutIdleSec=3600
[Install]
WantedBy=multi-user.target
```

## Step 4
Enable and start the service:
```bash
sudo systemctl enable mnt-rpi3.automount
sudo systemctl start mnt-rpi3.automount
sudo systemctl status mnt-rpi3.automount
```

If everything runs normally, browsing into `/mnt/rpi3` on your file manager should automatically mount your NAS drive without any prompt of any kind.

## Useful Links
[Arch WIKI - SMB](https://wiki.archlinux.org/title/samba#Client)  

[RPI3 NAS](https://adamtheautomator.com/raspberry-pi-nas/)

[Automount](https://unix.stackexchange.com/questions/283442/systemd-mount-fails-where-setting-doesnt-match-unit-name)
