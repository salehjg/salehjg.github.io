---
layout: post
title:  "Mutable Abstract Syntax Trees"
date:   2023-07-02 12:32:45 +0330
categories:
---

# Mutable Abstract Syntax Trees
## Abstract Syntax Tree (AST)
Abstract Syntax Trees or ASTs in short, are containers that represent a piece of code in a file or in some cases, the entirety of multiple files.
ASTs are the "abstract" versions of parse trees, but the line between parse trees and abstract ones is so thin that a C or C++ file might actually be fully reconstructed from its AST (meaning that the AST used is not that "abstract").
The quality of the reconstructed code from the AST is completely coupled with the amount of information stored in these containers.
The philosophy behind the design of ASTs enforces their immutable quality, meaning that if an AST is mutable (modifiable), the modified versions would no longer represent the actual code that it has been derived from. This is why most ASTs in open-source projects are designed to be immutable (at least to some extent).

## Parsers and ASTs
A parser is an important part of a compiler's front end. It takes tokens, generates instances of the required containers, and links them together to construct the root node of the actual code. 

## An example 
Have a look at the image below. It represents the class hierarchy of a C++ AST.
<img align="center" width="480" src="https://salehjg.github.io/cppparser/inherit_graph_0.png">
Every block is a `class` or a `structure`. When enough instances of these classes are linked together, they can fully represent a C++ code.

## What Now?
As you can guess, a parser is not the only class that can create ASTs. They could be assembled programmatically by anyone. Now, the problem is that the ASTs are designed to be immutable. What if someone wants to create a piece of C++ code from nothing? Of course, one can write a simple Python code to add pieces of strings to create the C++ code of interest but this approach poses a severe problem: **What if a name of a variable is to be changed? How do you find that variable declaration/definition and change the name there?**
In this context, a mutable AST makes sense. What if we modify an existing C++ front end and make its AST mutable? That might actually allow us to have its parser process our C++ code and generate our modified version of the AST. Now, not only you have a perfect data structure that represents the original code, but you also have a mutable tree that allows meaningful and easy modifications to take place.

## The bigger picture
Imagine that you have a dependency graph like the one below, and you want to generate a C++ code for it but with a catch. The catch is that you want to have multiple passes at this code, each time optimizing only a particular aspect of the code, just like the optimization passes implemented in modern compilers.
<img align="center" width="480" src="https://raw.githubusercontent.com/salehjg/salehjg.github.io/master/images/fused_2x_conv2d_valid_img2.PNG">
To achieve this, all we need to do is:
1. Choose a C++ front end, like `cppparser` [that I have forked](https://github.com/salehjg/cppparser/tree/my-master).
2. Modify its AST and make it mutable.
3. Write helper functions to create various AST structures easily.
4. Assemblee the AST.
5. Do your modifications to the AST in multiple passes.
6. Write a class to pretty-print the resulting AST back to C++ code.

## Expreiments
[Check out my fork](https://github.com/salehjg/cppparser/tree/my-master) of `cppparser`. This fork offers a mutable AST with some other changes.


