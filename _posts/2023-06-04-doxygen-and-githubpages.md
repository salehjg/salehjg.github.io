---
layout: post
title:  "Automated Doxygen deployment on Github Pages with diagrams"
date:   2023-06-04 12:32:45 +0330
categories:
---
<img align="right" width="150" src="https://www.doxygen.nl/images/doxygen.png">

# Automated Doxygen deployment on Github Pages with diagrams
It took me almost 5 hours to figure out how to use Github Actions to automatically build and deploy Doxygen documentation on Github Pages when commits are pushed into a Github repository.
There are some [basic tutorials out there](https://github.com/satu0king/Github-Documentation-With-Doxygen) but what I was really intereseted in was configuring Doxygen to use `PlantUML` and `Graphwiz/dot` to draw the class hierarchy, as well as some other handy diagrams.
Once you get used to the procedure, you can find your way around quite easily, but since I usually end up forgetting how I solved an specific issue, here I will go through the steps that one needs to do, in order to deploy a working Github Action for Doxygen with `PlantUML` and `Dot` support.

# Assumptions
Lets assume that:
- We have a basic CMake C++ project.
- The sources are located at `src` directory.
- The project has a lot of dependencies with no ready-to-use packages to install them from.

# Goals
We are trying to achieve these goals:
- Setup a Github Action to build and deploy Doxygen documentation on the repositorie's Github Page.
- The Action should be triggered on every push to the `main` branch of the repo.
- The Doxygen generated files should be hosted in the same repository but in a different branch that is automatically created in case it does not exists (`gh-pages`).
- The Action should not require installing all the dependencies that our project needs to compile, since we are not intrested in building the project, but to build the documentation of it.
- The Github Page to be accessibale at: `<USERNAME>.github.io/<REPOSITORYNAME>`

# Steps

## Create two Doxygen configs
Since we do not want the Doxygen config file to be dependent on configuring the CMake script and consequently, 
having all the project dependencies installed, we need to have two Doxygen config files, 
one for offile-building the project on the premises, another for the Github Action.

This is required since we want `PlantUML` and `Graphwiz/dot` support. 
The path to `plantuml.jar` and `dot` executable should be specified in the Doxygen config file. 

Usually, this is done using CMake and its `FindProgram()` and `FindFile()` functionalities 
(checkout these examples: 
[CGenCpp/cmake/FindPlantUML.cmake](https://github.com/salehjg/CGenCpp/blob/main/cmake/FindPlantUML.cmake),
[CGenCpp/cmake/FindDot.cmake](https://github.com/salehjg/CGenCpp/blob/main/cmake/FindDot.cmake)
)
but for Github Actions we want to isolate building the project from building the doxygen documentation in order to 
avoid installing all the dependencies that the project needs to be built.

So, have a `Doxygen.in` file that [looks like this](https://github.com/salehjg/CGenCpp/blob/main/Doxyfile.in) and another copy of it named `DoxygenGithubAction` that [looks like this](https://github.com/salehjg/CGenCpp/blob/main/DoxyfileGithubAction).
Store both files in the root directory of your repository.
Note that one can use `doxygen -g <FILENAME>` to generate a basic configuration file, but then the content should be modified further to meet the objectives.


**The important tags are as follows:**
- `INPUT`: The space-sperated list of the files and folders that should be processed by Doxygen. Put `README.md` here as well, if you want Doxygen to use it as the main page.
- `RECURSIVE`: Should be set to `ON`. This way the nested directories are also going to be scanned for sources.
- `PROJECT_NAME`
- `EXCLUDE_PATTERNS`: Could be used mutiple times as in `EXCLUDE_PATTERNS += */cmake-build-release/*` and `EXCLUDE_PATTERNS += */build/*` to exclude these directories from the scanning process.
- `HTML_OUTPUT`: Set it to `build/doc` where the output files are going to be stored in. Doxygen will create the last directory (`doc`) if it does not exist, but the `build` directory should exist.
- `GENERATE_LATEX`: Set to `NO`. We are not interested in generating a PDF file.
- `HAVE_DOT`: Set to `YES`. This is required to render the caller/calle diagrams.
- `UML_LOOK`: Set to `YES`. This is required to render the collaboration and inheritance diagrams.
- `CALL_GRAPH`: Set to `YES` to render the call dependency diagrams.
- `CALLER_GRAPH`: Set to `YES` to render the caller dependency diagrams.
- `DOT_IMAGE_FORMAT`: Set to `png:cairo:cairo`.
- `DOT_PATH`: Set to `/usr/bin/dot`. This is where the `dot` executable is usually stored in an Ubuntu image (in Github Actions).
- `PLANTUML_JAR_PATH`: Set to `/usr/share/plantuml/plantuml.jar`. This is where the `platuml.jar` file is stored in an Ubuntu image. For ArchLinux it is `/usr/share/java/plantuml/plantuml.jar`.

**The nice-to-have tags are as follows:"
- `JAVADOC_AUTOBRIEF`
- `MARKDOWN_SUPPORT`: Should be set to `YES`.
- `AUTOLINK_SUPPORT`
- `BUILTIN_STL_SUPPORT`
- `EXTRACT_ALL`
- `EXTRACT_PRIVATE`
- `EXTRACT_PRIV_VIRTUAL`
- `EXTRACT_PACKAGE`
- `EXTRACT_STATIC`
- `EXTRACT_LOCAL_METHODS`
- `EXTRACT_ANON_NSPACES`
- `USE_MDFILE_AS_MAINPAGE`: Set it to `README.md` to use it as the main page. Make sure that `README.md` is also present in `INPUT` tag.
- `SOURCE_BROWSER`
- `GENERATE_TREEVIEW`: Set to `YES` to have a tree view on the left hand side of the webpage.
- `USE_MATHJAX`: Set to `YES` to have the math formulas written in LaTeX math format rendered in the output HTML files.
- `TEMPLATE_RELATIONS`: Set to `YES`.

 
  

