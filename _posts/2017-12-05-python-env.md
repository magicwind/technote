---
layout: post
title:  "macOS的Python环境配置"
categories: python
---
macOS版本：10.12.6 Sierra

## 背景

在macOS上安装Python环境有多种方式，新手刚接触的时候难免有些困惑，什么方式才是最佳实践呢？

由于macOS Sierra上已经预装了Python2.7，所以一般都是直接安装Python3，这样系统里就有两个Python版本。

而且Python3已经相当成熟，Python2也会在两年内失去维护，所以目前的开发使用Python3环境。Python3最新的版本是3.6。

安装Python3的方法是使用Homebrew。

`brew install python3`

安装完后，使用python3和pip3就能使用python3。python和pip还是使用的系统自带的Python2.7。

另外还有多种安装Python3的方式是使用第三方工具，如pyenv和virtualenv。

pyenv和virtualenv是完全不同的工具，工作方式也有差异。

还有一些相关的工具，也会一一介绍。

## 工具
### pyenv

pyenv是一个bash扩展，不支持Windows。

Stackoverflow上的介绍是：

> Pyenv intercepts your calls to python, pip, etc., to direct them to one of several of the system python tool-chains. So you always have all the libraries that you have installed in the selected python version available - as such it is good for users who have to switch between different versions of python.

意思就是说pvenv可以管理系统里多个python版本。

### VirtualEnv
Stackoverflow上的介绍是：

> VirtualEnv, is pure python so works everywhere, it makes a copy of, optionally a specific version of, python and pip local to the activate environment which may or may not include links to the current system tool-chain, if it does not you can install just a known subset of libraries into that environment. As such it is almost certainly much better for testing and deployment as you know exactly which libraries, at which versions, are used and a global change will not impact your module.

意思是说virtualenv用来方便地管理某个python版本下，多个项目可以独立地使用不同的依赖包。

### venv或pyvenv（Python >= 3.3）
Stackoverflow上的介绍是：

> Note that from Python 3.3 onward there is a built in implementation of VirtualEnv called venv (with, on some installations a wrapper called pyvenv - this wrapper is deprecated in Python 3.6), which should probably be used in preference. To avoid possible issues with the wrapper it is often a good idea to use it directly by using /path/to/python3 -m venv desired/env/path or you can use the excellent py python selector on windows with py -3 -m venv desired/env/path. It will create the directory specified with desired/env/path configure and populate it appropriately. In general it is very much like using VirtualEnv.

意思是说venv是官方推出的用来替代VirtualEnv的工具。和VirtualEnv十分相似，推荐使用。还可以看下

[Python官网](https://docs.python.org/3/library/venv.html)
> The **venv** module provides support for creating lightweight “virtual environments” with their own site directories, optionally isolated from system site directories. Each virtual environment has its own Python binary (allowing creation of environments with various Python versions) and can have its own independent set of installed Python packages in its site directories.

创建虚拟环境：
`python3 -m venv /path/to/new/virtual/environment`

> Running this command creates the target directory (creating any parent directories that don’t exist already) and places a pyvenv.cfg file in it with a home key pointing to the Python installation from which the command was run. It also creates a bin (or Scripts on Windows) subdirectory containing a copy of the python binary (or binaries, in the case of Windows). It also creates an (initially empty) lib/pythonX.Y/site-packages subdirectory (on Windows, this is Lib\site-packages).

> Once a virtual environment has been created, it can be “activated” using a script in the virtual environment’s binary directory. The invocation of the script is platform-specific:

bash/zsh:
`$ source <venv>/bin/activate`

### VirtualEnvWrapper
VirtualEnvWrapper是VirtualEnv的包装，提供了更简单的命令，需要和VirtualEnv一起使用。

### pyenv-virtualenv
> installed by pyenv-installer, which gives PyEnv tools for managing and interfacing to VirtualEnv - with this you can have a base installation that includes more than one version of python and create isolated environments within each of them - Linux/OS-X. 

意思是说它是pyenv管理virtualenv的扩展。

### PyInstaller
> PyInstaller can take your python code, possibly developed & tested under VirtualEnv, and bundle it up so that it can run one platforms that do not have your version of python installed - Note that it is not a cross compiler you will need a Windows (virtual-)machine to build Windows installs, etc., but it can be handy even where you can be sure that python will be installed but cannot be sure that the version of python and all the libraries will be compatible with your code.

用途：用来打包Python程序。

## 总结
对于macOS系统来说，如果只需要使用Python2.7环境，使用系统自带的就好了，最多再安装一个virtualenv来管理多个项目。

如果需要使用最新的Python3.6的话，需要使用Homebrew来安装，然后直接使用venv就能为多个项目创建出独立的虚拟环境了。

如果需要同时使用Python3的多个版本的话，就需要使用pyenv来管理多个Python版本了。

所以virtualenv和virtualenvwrapper只需要在Python2.7的版本上或者配合pyenv的多个Python版本来使用。使用最新的Python3.6的话是不需要virtualenv的。

## 参考

1. [Stackoverflow](https://stackoverflow.com/questions/29950300/what-is-the-relationship-between-virtualenv-and-pyenv)
2. [Python最佳实践指南！](https://pythonguidecn.readthedocs.io/zh/latest/index.html)