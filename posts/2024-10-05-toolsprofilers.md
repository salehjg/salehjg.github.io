---
title: Useful Tools and Profilers for C/C++
date: 2024-10-05
tags: [profiling, tools]
summary: I often forget the names of the tools and programs that I have found useful when I need them. In this post, I am going to document them with a short…
---

# Profiling Tools
I often forget the names of the tools and programs that I have found useful when I need them. In this post, I am going to document them with a short description and links to their src/pages.

## Tracy
A full set of profiling libraries and a visualizing GUI. [Website](https://tracy.nereid.pl/)

## Perfetto
Similar to Tracy, with a browser-friendly visualizer. [Website](https://perfetto.dev/)

## HeapTrack
A fast alternative to Valgrind and Massif for Stack/Heap profiling in Linux. Available in Arch (in the Extra repository). [Website](https://github.com/kde/heaptrack)

## Sanitizers in GCC/LLVM/ICPX
Various sanitizers available as a part of the standard famous compilers out there. [Link1-Intel](https://www.intel.com/content/www/us/en/developer/articles/technical/find-bugs-quickly-using-sanitizers-with-oneapi-compiler.html), [Link2-Google](https://github.com/google/sanitizers/wiki/AddressSanitizerLeakSanitizer).

## DMTCP
Save the status of a program onto a file and resume running it later from the checkpoint file. [Website](https://github.com/dmtcp/dmtcp)

## PAPI
It could be used in C++ programs to profile only a segment of the code. [PAPI](https://github.com/icl-utk-edu/papi)

## LIKWID
Pronounced similarly to liquid and similar to PAPI, it provides more CLI tools and ways to profile CPU tasks and code. [LIKWID](https://github.com/rrze-hpc/likwid)

## NVTX, Intel ITT, RocTX
These libraries are used to place temporal tags (strings) to make profiling more controlled. For example, with NVTX tags, you can see when your code reaches a certain point in time in the timeline profiled with `nsight system`. 
Here are the links: [Nvidia NVTX](https://github.com/NVIDIA/NVTX), [Intel ITT](https://github.com/intel/ittapi), and [AMD RocTX](https://github.com/ROCm).

