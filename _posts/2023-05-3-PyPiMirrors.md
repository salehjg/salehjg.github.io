---
layout: post
title:  "PyPI Mirrors"
date:   2023-05-3 12:32:45 +0330
categories:
---
<img align="right" width="150" src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/PyPI_logo.svg/1200px-PyPI_logo.svg.png">


# PyPI Mirrors
If your `pip` is slow dowloading the packages you might want to use a PyPI mirror. The unfortunate issues is that unlike other package managers there is no central mirror list on any of the PyPI's webpages or at least it is so vague that I could not find one. Long story short, here is the list of the working mirrors that I have found so far. Please note that the commands above will only force `pip` to use the given mirror temporarily. For more details, please refer to [this link](https://mirrors.sustech.edu.cn/help/pypi.html#_2-configure-index-url).

**WARNING:** I do not trust any of the listed mirrors below and I would rather try to set up a better network connection and/or use a VPN. Take special care using `repo.ito.gov.ir`, since it belong to Ministry of Information and Communications Technology of Iran (well, you can guess the rest :) ). 
  
```bash
sudo pip3 config set global.index-url https://mirror.sjtu.edu.cn/pypi/web/simple
sudo pip3 config set global.index-url https://mirrors.sustech.edu.cn/pypi/simple
sudo pip3 config set global.index-url https://repo.ito.gov.ir/python 
```
  

