---
layout: post
title:  "A Tool To Convert Mesh Data To Pointcloud"
date:   2021-09-10 12:32:45 +0330
categories:
---

<img align="right" width="150" src="https://raw.githubusercontent.com/salehjg/MeshToPointcloudFPS/master/data/image.png">

[MeshToPointcloudFPS](https://github.com/salehjg/MeshToPointcloudFPS) is an opensource utility based on [PCL-lib](https://github.com/PointCloudLibrary/pcl), [Vcglib](https://github.com/cnr-isti-vclab/vcglib), and [Meshlab](https://github.com/cnr-isti-vclab/meshlab) to convert `OBJ` files into `PCL` or `HDF5` files. It supports downsampling of the resulted pointcloud using Furthest Point Sampling (FPS) algorithm. The utility could be used to prepare datasets offered in Mesh format (such as Shapenet Core).

```
$ FpsCpu -h
Usage: FpsCpu [options...]
Options:
    -i, --inputmesh        The path for the input mesh *.obj file. (Required)
    -o, --outputhdf5       The path for the output hdf5 *.h5 file with sampled point cloud. (Required)
    -n, --npoints          The target number of points per mesh input file (input.obj). (Required)
    -r, --rawpcd           The path for the optional output pcd *.pcd file with RAW point cloud.
    -p, --outputpcd        The path for the optional output pcd *.pcd file with sampled point cloud.
    -h, --help             Shows this page 
```
