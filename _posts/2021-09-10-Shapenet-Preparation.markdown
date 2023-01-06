---
layout: post
title:  "Preparation of Shapenet Core V2 (Mesh to PCL) "
date:   2021-09-10 12:32:45 +0330
categories:
---

<img align="right" width="150" src="https://raw.githubusercontent.com/salehjg/MeshToPointcloudFPS/master/data/image.png">

This post is going to be a short one! Just wanted to share [my python script](https://github.com/salehjg/Shapenet2_Preparation) to prepare and convert [Shapenet Core V2](https://shapenet.org/) to pointclouds. 
It is based on [MeshToPointcloudFPS](https://github.com/salehjg/MeshToPointcloudFPS) utility and is capable of launching multiple tasks to saturate the CPU cores.
The output will be in HDF5 format and the script will take care of splitting the dataset for train-val-test sets.
