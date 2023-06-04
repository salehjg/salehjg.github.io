---
layout: post
title:  "Automated Doxygen deployment on Github Pages with diagrams"
date:   2023-06-04 12:32:45 +0330
categories:
---
<img align="right" width="150" src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png">

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
(checkout these examples: [FindPlantUML.cmake](https://github.com/salehjg/CGenCpp/blob/main/cmake/FindPlantUML.cmake), [FindDot.cmake](https://github.com/salehjg/CGenCpp/blob/main/cmake/FindDot.cmake))
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


**The nice-to-have tags are as follows:**
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

## Create `main.yml`:
Create the hidden `.github` folder. Inside, create another folder named `workflows`. (`mkdir -p .github/workflows`)
Then create a file named `main.yml` inside `workflows` directory with the content:
~~~
# This is a basic workflow to help you get started with Actions

name: Doxygen Action

# Controls when the action will run. Triggers the workflow on push or pull request
# events but only for the master branch
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]


  
# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  # This workflow contains a single job called "build"
  build:
    # The type of runner that the job will run on
    runs-on: ubuntu-latest

    # Steps represent a sequence of tasks that will be executed as part of the job
    steps:
    # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
    - uses: actions/checkout@v3.5.2

    - name: Install plantuml
      run: sudo apt-get update && sudo apt-get install -y plantuml

    - name: actions-setup-cmake
      uses: jwlawson/actions-setup-cmake@v1.14.0
      with:
        cmake-version: 'latest'
    
    - name: configure our build dir
      run: mkdir -p build/doc

    - name: Doxygen Action
      uses: mattnotmitt/doxygen-action@v1.9.5
      with:
        # Path to Doxyfile
        doxyfile-path: "./DoxyfileGithubAction"
        # Working directory
        working-directory: "."
    
    - name: Deploy
      uses: peaceiris/actions-gh-pages@v3.9.3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ${{ github.workspace }}/build/doc
~~~

1. Set your master branch's name in `branches: [<HERE>]`. Mine is called `main`.
2. Set the image name to Ubuntu with `runs-on: ubuntu-latest`. We have hardcoded the paths to `plantuml.jar` and `dot` in the Doxygen config file for an Ubuntu image, so we need to use Ubuntu here.
3. Use `actions/checkout` so you can access your repository in `$GITHUB_WORKSPACE` or `${{ github.workspace }}`.
4. Install `plantuml` with `sudo apt-get update && sudo apt-get install -y plantuml`.
5. (you might have to install `mathjax` as well.
6. Install `cmake` with `jwlawson/actions-setup-cmake` in case you do not want to hardcode the files paths into the Doxygen config file. (NOT NEEDED HERE)
7. Setup our output directories with `mkdir -p build/doc`.
8. Use `mattnotmitt/doxygen-action` to handle Doxygen generation. Set `doxyfile-path` to `./DoxyfileGithubAction`. Do not forget that our relative path is based on the `working-directory` which is set to `.`, meaning the root directory of your repository copy on the server.
9. Use `peaceiris/actions-gh-pages` to automatically publish the content of `<ROOT REPO DIR>/build/doc` on the repositorie's Github Page. Set `publish_dir` to `${{ github.workspace }}/build/doc`. It will handle creating the `gh-pages` branch and pushing the files there.
10. On your local machine, commit the changes and push it to Github.
11. Wait for the Action to finish.
12. Make sure there are no errors.
13. Go to your Github repository, click on the `Settings` menu, click on `Pages` from the left menu bar, select `Deploy from a branch` for `Sources`. Finally, select `gh-pages` and `Root /` for the branch combo-boxes.
14. You might need to allow Actions to write into your repository. Github Repo -> Settings -> Actions -> General: Select `Read and Write Permissions` radio-button and check the `Allow Github Actions to create and approve pull requests` checkbox.

## Have a cup of coffee and enjoy the results
Now, you can access the deployed Github Page of the repository at `https://<USERNAME>.github.io/<REPO NAME>`.

# References
[actions-gh-pages](https://github.com/peaceiris/actions-gh-pages)
[doxygen-action](https://github.com/mattnotmitt/doxygen-action)
[Github-Documentation-With-Doxygen](https://github.com/satu0king/Github-Documentation-With-Doxygen)
[learn-github-actions](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions)
[CGenCpp](https://github.com/salehjg/CGenCpp)
