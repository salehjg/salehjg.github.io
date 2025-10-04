---
layout: post
title:  "oneAPI icpx crashes when using the cache config extension"
date:   2025-10-04 12:32:45 +0330
categories: oneapi
---

# oneAPI icpx crashes when using the cache config extension

When experimenting with the [Intel SYCL cache configuration extension](https://github.com/intel/llvm/blob/sycl/sycl/doc/extensions/experimental/sycl_ext_intel_cache_config.asciidoc), I noticed that `icpx` crashes during compilation or produces an executable that crashes at runtime. 
The problem shows up when the `sycl::ext::intel::experimental::cache_config` attribute is used in a kernel. This seems to point to an issue or incomplete support for the extension in the current `icpx` toolchain. 
It’s easy to reproduce with a small SYCL example. 
I managed to reproduce the problem on `oneAPI 2025.0.1` and `2025.2.1`. To my surprise, `oneAPI 2025.1.0` works fine and is unaffected by this issue.


## Sample Code
```
#include <chrono>
#include <iostream>
#include <cassert>
#include <cmath>
#include <sycl/sycl.hpp>

constexpr size_t MATRIX_DIM = 1 << 11;
constexpr size_t MATRIX_ELEMENTS = MATRIX_DIM * MATRIX_DIM;
constexpr size_t TILE_SIZE = 16;
constexpr size_t STEPS = 100;

static_assert(MATRIX_DIM % TILE_SIZE == 0, "Matrix dimension must be divisible by tile size");

namespace expo = sycl::ext::oneapi::experimental;
namespace expp = sycl::ext::intel::experimental;

template<expp::cache_config_enum Config>
float run(sycl::queue& queue) {
    float* mat_a = sycl::malloc_device<float>(MATRIX_ELEMENTS, queue);
    float* mat_b = sycl::malloc_device<float>(MATRIX_ELEMENTS, queue);
    float* mat_c = sycl::malloc_device<float>(MATRIX_ELEMENTS, queue);

		expo::properties props = expo::properties{expp::cache_config{Config}};

    queue.fill(mat_a, 1.0f, MATRIX_ELEMENTS);
    queue.fill(mat_b, 2.0f, MATRIX_ELEMENTS);
    queue.fill(mat_c, 0.0f, MATRIX_ELEMENTS);
    queue.wait();

    auto start = std::chrono::high_resolution_clock::now();

    queue.submit([&](sycl::handler& cgh) {
        sycl::local_accessor<float, 2> tile_a({TILE_SIZE, TILE_SIZE}, cgh);
        sycl::local_accessor<float, 2> tile_b({TILE_SIZE, TILE_SIZE}, cgh);

        cgh.parallel_for(
            sycl::nd_range<2>{sycl::range<2>{MATRIX_DIM, MATRIX_DIM}, sycl::range<2>{TILE_SIZE, TILE_SIZE}},
            // props,
            [=](sycl::nd_item<2> item) {
                const size_t global_row = item.get_global_id(0);
                const size_t global_col = item.get_global_id(1);
                const auto local_id = item.get_local_id();
                const size_t local_row = local_id[0];
                const size_t local_col = local_id[1];

								for (auto _ = 0; _ < STEPS; _++) {
									float acc = 0.0f;

									for (size_t tile = 0; tile < MATRIX_DIM; tile += TILE_SIZE) {
											// Stage tiles in local memory so each work-item can reuse operands.
											tile_a[local_id] = mat_a[global_row * MATRIX_DIM + tile + local_col];
											tile_b[local_id] = mat_b[(tile + local_row) * MATRIX_DIM + global_col];

											item.barrier(sycl::access::fence_space::local_space);

											for (size_t k = 0; k < TILE_SIZE; ++k) {
													acc += tile_a[sycl::id<2>(local_row, k)] * tile_b[sycl::id<2>(k, local_col)];
											}

											item.barrier(sycl::access::fence_space::local_space);
									}

									mat_c[global_row * MATRIX_DIM + global_col] = acc;
								}

            });
    }).wait();

    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double, std::milli> duration = end - start;

    sycl::free(mat_a, queue);
    sycl::free(mat_b, queue);
    sycl::free(mat_c, queue);

    return duration.count();
}

int main() {
    sycl::queue queue{sycl::gpu_selector_v};
    size_t iters = 10;

    std::cout << "Running on " << queue.get_device().get_info<sycl::info::device::name>() << std::endl;

    std::cout << "Cache config: Large Data" << std::endl;
    for (size_t i = 0; i < iters; ++i) {
        auto time = run<expp::cache_config_enum::large_data>(queue);
        std::cout << " Iteration " << i << ": " << time << " ms" << std::endl;
    }

    std::cout << "Cache config: Large SLM" << std::endl;
    for (size_t i = 0; i < iters; ++i) {
        auto time = run<expp::cache_config_enum::large_slm>(queue);
        std::cout << " Iteration " << i << ": " << time << " ms" << std::endl;
    }
}

```

## Build command to reproduce the problem (first)
```
icpx -std=c++17 -fsycl \
  -fsycl-targets=spir64_gen \
  -Xsycl-target-backend "-device pvc" \
  main.cpp -o main
```
This will lead to compiler crashing without generating the output:
```
Intel(R) oneAPI DPC++/C++ Compiler for applications running on Intel(R) 64, Version 2025.2.1 Build 20250806
Copyright (C) 1985-2025 Intel Corporation. All rights reserved.

Compilation from IR - skipping loading of FCL
[0]: /lib64/libocloc.so(_ZN16SafetyGuardLinux9sigActionEiP9siginfo_tPv+0x34) [0x14880dc0af04]
[1]: /lib64/libc.so.6(+0x54df0) [0x14880d854df0]
[2]: /lib64/libigc.so.1(+0xc387a2) [0x148808c387a2]
[3]: /lib64/libigc.so.1(+0xc3916b) [0x148808c3916b]
[4]: /lib64/libigc.so.1(_ZN4llvm13FPPassManager13runOnFunctionERNS_8FunctionE+0x2a4) [0x148809537124]
[5]: /lib64/libigc.so.1(_ZN4llvm13FPPassManager11runOnModuleERNS_6ModuleE+0x2c) [0x14880953740c]
[6]: /lib64/libigc.so.1(_ZN4llvm6legacy15PassManagerImpl3runERNS_6ModuleE+0x319) [0x148809538859]
[7]: /lib64/libigc.so.1(+0x96b9f0) [0x14880896b9f0]
[8]: /lib64/libigc.so.1(+0x96bfbf) [0x14880896bfbf]
[9]: /lib64/libigc.so.1(+0x934919) [0x148808934919]
[10]: /lib64/libigc.so.1(+0xa5a0fb) [0x148808a5a0fb]
[11]: /lib64/libigc.so.1(+0x936877) [0x148808936877]
[12]: /lib64/libigc.so.1(+0xa33cd9) [0x148808a33cd9]
[13]: /lib64/libigc.so.1(+0xa3537f) [0x148808a3537f]
[14]: /lib64/libocloc.so(_ZN3NEO15OfflineCompiler15buildSourceCodeEv+0x51b) [0x14880dbf6bcb]
[15]: /lib64/libocloc.so(_ZN3NEO15OfflineCompiler5buildEv+0x45) [0x14880dbf7095]
[16]: /lib64/libocloc.so(+0xd336b) [0x14880dc0e36b]
[17]: /lib64/libocloc.so(_Z20buildWithSafetyGuardPN3NEO15OfflineCompilerE+0xbb) [0x14880dc0e44b]
[18]: /lib64/libocloc.so(_ZN5Ocloc8Commands7compileEP14OclocArgHelperRKSt6vectorINSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEESaIS9_EE+0x108) [0x14880dbf85c8]
[19]: /lib64/libocloc.so(oclocInvoke+0x4fc) [0x14880dbea0cc]
[20]: /usr/bin/ocloc(main+0x27) [0x55e5c961a747]
[21]: /lib64/libc.so.6(+0x3feb0) [0x14880d83feb0]
[22]: /lib64/libc.so.6(__libc_start_main+0x80) [0x14880d83ff60]
[23]: /usr/bin/ocloc(_start+0x25) [0x55e5c961a775]
llvm-foreach: Aborted (core dumped)
icpx: error: gen compiler command failed with exit code 254 (use -v to see invocation)
Intel(R) oneAPI DPC++/C++ Compiler 2025.2.1 (2025.2.0.20250806)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /home/userexternal/xxxx/intel/oneapi2025.2.1/compiler/2025.2/bin/compiler
Configuration file: /home/userexternal/xxxx/intel/oneapi2025.2.1/compiler/2025.2/bin/compiler/../icpx.cfg
icpx: note: diagnostic msg: Error generating preprocessed source(s).
```

## Build command to reproduce the problem (second)
```
icpx -std=c++17 -fsycl main.cpp -o main
```
This will generate the output without any error but the executable crashes on runtime:

```
Running on Intel(R) Data Center GPU Max 1100
Cache config: Large Data
Segmentation fault (core dumped)
```


## Affected versions
- **The versions that are broken**: oneAPI Base Toolkit 2025.2.1 and 2025.0.1 (tested these ones)
- **The version that works fine**: oneAPI Base Toolkit 2025.1.0

## Hardware
Two Intel Max 1100 (we are using one)

```

$sycl-ls
[level_zero:gpu][level_zero:0] Intel(R) oneAPI Unified Runtime over Level-Zero, Intel(R) Data Center GPU Max 1100 12.60.7 [1.3.26918]
[level_zero:gpu][level_zero:1] Intel(R) oneAPI Unified Runtime over Level-Zero, Intel(R) Data Center GPU Max 1100 12.60.7 [1.3.26918]
[level_zero:gpu][level_zero:2] Intel(R) oneAPI Unified Runtime over Level-Zero, Intel(R) Data Center GPU Max 1100 12.60.7 [1.3.26918]
[level_zero:gpu][level_zero:3] Intel(R) oneAPI Unified Runtime over Level-Zero, Intel(R) Data Center GPU Max 1100 12.60.7 [1.3.26918]
[opencl:cpu][opencl:0] Intel(R) OpenCL, Intel(R) Xeon(R) Platinum 8480+ OpenCL 3.0 (Build 0) [2025.20.8.0.06_160000]
[opencl:gpu][opencl:1] Intel(R) OpenCL Graphics, Intel(R) Data Center GPU Max 1100 OpenCL 3.0 NEO  [23.30.26918.50]
[opencl:gpu][opencl:2] Intel(R) OpenCL Graphics, Intel(R) Data Center GPU Max 1100 OpenCL 3.0 NEO  [23.30.26918.50]
[opencl:cpu][opencl:3] Intel(R) OpenCL, Intel(R) Xeon(R) Platinum 8480+ OpenCL 3.0 (Build 0) [2024.18.7.0.11_160000]
```







