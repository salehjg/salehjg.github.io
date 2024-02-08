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
Connect the device with USB to your host. The IP address of the device should be `172.16.42.1`.  
PostmarketOS uses Network Filter Tables. Please refer to [this page](https://wiki.postmarketos.org/wiki/Firewall) for more info.  
The rules for allowing or blocking ports could be found at `/etc/nftables.d/`. For example, to allow SMB:   
```
sudo nano /etc/nftables.d/50-smb.nft
```
Then paste these into the file and save it:  
```
#!/usr/sbin/nft -f

table inet filter {
	chain input {
		# allow ssh
		tcp dport 22 accept comment "accept SSH"
	}
}
```
And finally, to reload the rules, run:  
```
sudo rc-service nftables restart
```

## SD Card
The device name for SD-card for mido is `mmcblk1` in my case. For a quick setup, you can format and automount it like this:  
```
sudo fdisk /dev/mmcblk1  # create a single partition in the SD-card.
sudo mkfs.ext4 /dev/mmcblk1p1  # this will wipe the device, careful!
sudo mkdir /mnt/sdcard
sudo chown $USER /mnt/sdcard/
```
Now, edit your fstab to automount the partition on system boot:  
```
/dev/mmcblk1p1    /mnt/sdcard    ext4    defaults    0    0
```

## Battery Life
You can use a bash script such as this:  
```
echo "Battery: $(sudo cat /sys/class/power_supply/qcom-battery/capacity) -- $(sudo cat  /sys/class/power_supply/qcom-battery/status)"
```


## Samba Server
Install Samba:
```
sudo apk add samba-server
sudo smbpasswd -a $USER
sudo nano /etc/samba/smb.conf
```

Then paste these configurations:  
```
[global]
   workgroup = MYGROUP
   server string = Samba Server
   server role = standalone server
   log file = /var/log/samba/%m.log
   max log size = 50
   interfaces = wlan0 usb0
   dns proxy = no
   socket options = TCP_NODELAY IPTOS_LOWDELAY SO_RCVBUF=2048000 SO_SNDBUF=2048000

[internal]
;  comment = My SMB server on mido
   path = /home/saleh/00_shared
;  valid users = saleh
   public = no
   writable = yes
   printable = no
;  create mask = 0765

[sdcard]
;  comment = My SMB server on mido
   path = /mnt/sdcard
;  valid users = saleh
   public = no
   writable = yes
   printable = no
;  create mask = 0765

```
(Replace `saleh` with your username, make sure you have `/home/saleh/00_shared`. Note that `interfaces = wlan0 usb0` forces `smbd` to bind to the both interfaces.)

And finally, to reload the config, run:  
```
sudo rc-service samba restart 
sudo rc-update add samba  # enable the service on system boot
sudo cat /var/log/samba/smbd.log  # to see if there were any errors.
```

When all set, reboot the device with `sudo reboot` and see if you have the SMB share accessible from the host:  
```
sudo mount -t cifs //172.16.42.1/internal /mnt/mido/internal/ -o nobrl,username=xxxxxx,password=xxxxxxx,workgroup=WORKGROUP,iocharset=utf8,uid=1000,gid=1000

sudo mount -t cifs //172.16.42.1/sdcard /mnt/mido/sdcard/ -o nobrl,username=xxxxxxx,password=xxxxxxx,workgroup=WORKGROUP,iocharset=utf8,uid=1000,gid=1000
```

Please note that you have to change `xxxxxx` with your credentials. Also, to disable byte-range locking that causes issues with Zotero, I have added `nobrl` to the options. Without it, Zotero would hang after opening the database without any errors.


