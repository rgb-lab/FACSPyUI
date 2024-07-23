# FACSPyUI
PyQT Interface for FACSPy

## Installation
Currently, FACSPy and FACSPyUI are in beta phase. A pypi distribution will be available once the beta phase is completed.

To install, first clone this repository to your local drive via your terminal:

```shell
>>> git clone https://github.com/TarikExner/FACSPyUI.git
```

It is recommended to choose conda as your package manager. Conda can be obtained, e.g., by installing the Miniconda distribution, for detailed instructions, please refer to the respective documentation.

With conda installed, open your terminal and create a new environment by executing the following commands.
```shell
>>> conda create -n facspyui python=3.10
>>> conda activate facspy
```

First, install all dependencies. For FACSPy, use the github repo.
```shell
>>> pip install git+https://github.com/TarikExner/FACSPy@main
>>> pip install pyqt5 plotly pyinstaller PyQtWebEngine
```

In order to run the app locally , navigate to the folder FACSPyUI and type
```shell
>>> python FACSPyUI.py
```
Note that currently you have to be in the same directory.


In order to build it yourself, navigate to the directory and run:
```shell
>>> pyinstaller app.spec
```

If that doesnt work due to a command-not-found, reinstall pyinstaller with:
```shell
>>> pip install --upgrade pyinstaller
```

If you want to use pre-existing builds, choose one of the following links.

