---
layout: post
title:  "Using Cereal library for serializing objects in C++"
date:   2023-04-10 12:32:45 +0330
categories:
---
<html lang="en">
   <head>
	 <script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/8.0.0/mermaid.min.js"></script>
    </head>
	 
<body>
 <pre><code class="language-mermaid">graph LR
A--&gt;B
</code></pre>

<div class="mermaid">graph LR
A--&gt;B
</div>
	
</body>
<script>
var config = {
    startOnLoad:true,
    theme: 'forest',
    flowchart:{
            useMaxWidth:false,
            htmlLabels:true
        }
};
mermaid.initialize(config);
window.mermaid.init(undefined, document.querySelectorAll('.language-mermaid'));
</script>

</html>

# Using Cereal library for serializing objects in C++
<img align="right" width="150" src="https://uscilab.github.io/cereal/assets/img/cerealboxside.png">
Hi there, I just wanted to share my simple CMake example of how to use `Cereal` to serialize classes considering inheritances and polymorphism.
Long story short, we have 3 classes inherited from the base-class as shown below. 
We are also using `STL smart pointers` meaning that `Cereal` should be able to detect the type of the pointee that a base-class pointer points to. As it turns out it is quite simple to define the structure of our inheritance and help `Cereal` understand it.
[Here is a link to my Github repository.](https://github.com/salehjg/Cereal-Cpp-Examples/blob/main/readme.md)

```mermaid
graph TD;
  CConst-->CSymbolic;
  CSymbol-->CSymbolic;
  CSymLink-->CSymbolic;
```
