---
layout: default
---

[Home](index.html) | [Documentation](documentation.html) | [Install on linux](install-on-linux.html) | [Install on windows](install-on-windows.html)

## Installing Kissenium on windows

To have Kissenium running on windows, you will need to have python3, pip3, ffmpeg and git installed.

We will go trough the installation of theses dependencies.

### Installing python3 and pip3

To install python3, you have to go the download page of the [python website](https://www.python.org/downloads/), and get latest python3 installer (3.6.2 when creating this page).

When you have downloaded it, choose custom installation. In the custom installation, check all checkboxes in "Optional features" screen, and be sure that the "Add python to environment variables" is checked in the "Advanced options" screen.

No open a windows terminal and type `python`. If a python3 console show up, your good to go. If not, check your environment variables.

From a terminal :

```bash
pip3 install --upgrade virtualenv
```

### Installing git

Go to the git for windows [download](https://git-scm.com/download/win) page, and install it. 

After the installation, run git-bash and type in it `ssh-keygen`.

It will create your ssh key: without it you won't be able to clone the repository.

### Installing ffmpeg

Download ffmpeg from the [windows download page](http://ffmpeg.zeranoe.com/builds/) and extract it to `C:\ffmpeg`.

Open your system path variable and add `C:\ffmpeg\bin` to it.

Now, if you open a terminal and you type `ffmpeg -version`, ffmpeg should show you a response.

### Installing Kissenium

Open a terminal a clone the kissenium repository: `git clone git@github.com:AdiuvoDotFr/Kissenium.git kissenium` or download it from `https://github.com/AdiuvoDotFr/Kissenium/zipball/master`.

Open a terminal and go to the kissenium folder :

```bash
python -m venv .

Scripts\activate.bat
pip3 install -r requirements.txt
```

Now Kissenium is installed on your system. To launch it, and the demo test if you do not have modified the tests, you have to type the following command :

```bash
python kissenium.py
```

Now, please refer to the [documentation page](documentation.html) to learn a little about how to work with Kissenium.

