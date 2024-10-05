---
layout: post
title:  "Useful Tools and Profilers for C/C++"
date:   2024-10-05 12:32:45 +0330
categories: profiling
---
# Profiling Tools
I often forget the names of the tools and programs that I have found useful when I need them. In this post, I am going to document them with a short description and links to their src/pages.

## Tracy
A full set of profiling library and visualizing GUI. [Website](https://tracy.nereid.pl/)

## Perfetto
Similar to Tracy, with a browser friendly visualizer. [Website](https://perfetto.dev/)

## HeapTrack
A fast alternative to Valgrind and Massif for Stack/Heap profiling in Linux. Available in Arch (in Extra repository). [Website](https://github.com/kde/heaptrack)

## Sanitizers in GCC/LLVM/ICPX
Various sanitizers available as a part of the standard famous compilers out there. [Link1-Intel](https://www.intel.com/content/www/us/en/developer/articles/technical/find-bugs-quickly-using-sanitizers-with-oneapi-compiler.html), [Link2-Google](https://github.com/google/sanitizers/wiki/AddressSanitizerLeakSanitizer).

## DMTCP
Save the status of a program onto a file and resume running it later from the checkpoint file. [Website](https://github.com/dmtcp/dmtcp)

