Introduction
===
These workshops are intended to help bolster some basic coding skills. Formal [CS training](https://www1.cs.ucr.edu/undergraduate/course-descriptions#CS009A) like an introduction to computer science is also useful if this is new to you and you want to master a more formal programming expertise. That said, many biologists are self taught through workshops and experience so you don't need start with a formal class to get started.

There are many online resources available for learning programming and I would suggest referring to these when you find that concepts need more background
* [MIT: CS 6.00001](https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/)
* [Software Carpentry: Intro to Python](https://swcarpentry.github.io/python-novice-inflammation/)
* [Software Carpentry: Plotting and Programming in Python](http://swcarpentry.github.io/python-novice-gapminder/)
* [Software Carpentry: Intro to R](http://swcarpentry.github.io/r-novice-inflammation/)
* [Software Carpentry: R for Reproducible Scientific Analysis](https://swcarpentry.github.io/r-novice-gapminder/)

Other workshops around data organization, Genomics are useful
* [Data Carpentry: Genomics](https://datacarpentry.org/lessons/#genomics-workshop)
* [Data Carpentry: Ecology](https://datacarpentry.org/lessons/#ecology-workshop) - includes Datases

Make sure you are using a good Integrated Development Environments (IDE)
===

I have found [Visual Studio](https://code.visualstudio.com/) has been a really useful tool, especially as [Atom](https://atom.io) sunsetted.  VS allows you to write and format code in many different languages, and setup remote connections to linux and other hosts via SSH.  

* [Introduction to VStudio](https://code.visualstudio.com/docs)
* You can [render and edit](https://code.visualstudio.com/docs/languages/markdown) Markdown code to nicely debug as your writing.
* really nice [python](https://code.visualstudio.com/docs/languages/python) interface including running python directly in test. I like this better than python notebooks but you all will have preferences

You can also use [jupyter notebook and editor](https://jupyter.hpcc.ucr.edu) on the cluster. This supports a simple editor (click on text files in the file navigator or use the open file option) as well as setting up python notebooks where you can directly type and run python code in persistent environments. 


as well as [Rstudio](https://rstudio.hpcc.ucr.edu) (and also [second Rstudio server](https://rstudio2.hpcc.ucr.edu)) - there are free RStudio (now posit) virtual machines which work well for teaching and stand alone like [posit (Formally rcloud)](https://posit.cloud/). You can [run Rstudio/Posit locally](https://posit.co/) to your laptop as well.

How to use git
===
Version control is important way to share the code, archive it, collaborate, and ensure reproducibility of your work.

For now here are a few tutorials to work on your own.

One query has been how to start a repository after already coding something up. Go to the base folder for your project (eg top-level folder that contains your project info) and initialize a repository.

```bash
git init
```
After doing this, go to your github (for lab projects that will be published it is better to create them within the [lab organization](https://github.com/stajichlab)) - click on ['New'](https://github.com/organizations/stajichlab/repositories/new) and then make sure the 'Owner' is 'stajichlab' otherwise if this is a repository for something experimental or where you want primary to be your own account you can choose your account.  Here's a map for some of the other lab organizations:
* [Citrus ECDRE](https://citrus-hlb-micro.github.io/) project we use the `Citrus-HLB-Micro` org
* [1000 genomes](https://1000.fungalgenomes.org) we use `1kfg` org
* [zygomycete genomics](https://zygolife.org) we use `zygolife` org
* [Herptile Microbiomes](https://herptilemicrobiomes.org) we use `herptilemicrobiomes` org
* [Dryland microbiomes](https://github.com/drylandmicrobes) for dryland collaborative projects `drylandmicrobes`

How to standardize code
=== 
[Linting](https://en.wikipedia.org/wiki/Lint_(software)) is running a separate tool checks your code is following standards (like consistent space/tab for python), and also enforcing spaces after commas. 

There are a couple of tools for python linting, pep8 and flake8 are useful. In Visual studio you can install.

Within git there are a series of actions you can run before code is checked in (pre-commits) as well as after code is committed (post-commit). The post-commit is how for example the github hosted websites which require additional steps to be run to deploy it, can be generated. This is how the lab website setup is done with [Actions](https://github.com/stajichlab/stajichlab.github.io/actions). 

For pre-commit this will commit a file in your github repository home (`.pre-commit-config.yaml`) - see this one for [AAFTF](https://github.com/stajichlab/AAFTF/blob/main/.pre-commit-config.yaml). This was initially created by running the tool `pre-commit` which is installed either via your own conda env and pip (eg `pip install pre-commit`) or you can use one already put in the `biopython` conda env - so do 
```bash
module load bioconda
pre-commit
```

Once this is setup, the precommit steps that include flake8 linting for python, a file size checking so you don't try to commit files beyond a specified size, 

