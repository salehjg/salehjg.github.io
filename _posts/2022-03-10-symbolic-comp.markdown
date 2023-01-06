---
layout: post
title:  "Mature Libraries for Symbolic Computation"
date:   2022-03-10 12:32:45 +0330
categories:
---

Lately, shortcomming of `SymPy` for Python has forced me to look for its alternatives elsewhere.
Based on [the comments that I got from the Reddit community](https://www.reddit.com/r/cpp/comments/t8zjww/a_mature_library_for_symbolic_computation/), it seems like the libraries listed below could be some good alternatives for various languages.


| **Name**       | **Biased Notes**      | **Wrapper**         | **Core** | **Year** | **Web**                                                    |
|----------------|-----------------------|---------------------|----------|----------|------------------------------------------------------------|
| Sympy          | Slow                  | -                   | Python   | 2022     | [Link](https://www.sympy.org/en/index.html)                |
| SymEngine      | Fast, Lacking Features| Python              | C++      | 2022     | [Link](https://github.com/Symengine)                       |
| SageMath       | Sympy Backend (Slow?) | ?                   | ?        | 2022     | [Link](https://www.sagemath.org/)                          |
| ViennaMath     | Not Being Maintained  | -                   | C++      | 2012     | [Link](https://sourceforge.net/projects/viennamath/files/) |
| SymbolicC++    | Not Being Maintained  | -                   | C++      | 2010     | [Link](https://en.m.wikipedia.org/wiki/SymbolicC%2B%2B)    |
| GiNaC          |                       | Python (incomplete) | C++      | 2022     | [Link](https://www.ginac.de/ginac.git/)                    |
| FORM           |                       | -                 |   C++      | 2021  | [Link](https://github.com/vermaseren/form)       |
| Maxima         |                       | ?                   | Lisp     | 2022     | [Link](https://maxima.sourceforge.io/download.html)        |
| JuliaSymbolics |                       | -                   | Julia    | 2022     | [Link](https://github.com/JuliaSymbolics/)                 |
