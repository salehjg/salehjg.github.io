---
layout: post
title:  "Nvidia Prime"
date:   2024-02-14 12:32:45 +0330
categories:
---
<img align="right" width="150" src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/NVIDIA_logo.svg/1920px-NVIDIA_logo.svg.png">

# Setting-up Nvidia Prime (Archlinux)
```
sudo pacman -S mesa mesa-utils nvidia-lts nvidia-prime nvidia-settings nvidia-utils
sudo pacman -R xf86-video-nouveau bumblebee
reboot
# sudo nvidia-xconfig --prime # only if you are not using wayland
yay -S nvtop optimus-manager  # just install optimus-manager, you dont have to use it, it will sort out some issues silently.
reboot
```
  
Then, verify the current GPU used with:
```
glxinfo -B
```
To run anything with Nvidia GPU, do:
```
prime-run glxinfo -B
```
Likewise, you can verify everything with:
```
glxgears -info
prime-run glxgears -info
```

While running those, you can open a new terminal and run the following command to monitor the GPUs:
```
nvtop
```

