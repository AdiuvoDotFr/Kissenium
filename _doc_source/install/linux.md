## Linux

To install Kissenium on linux you will need to have python3, pip3 and ffmpeg installed.

We choosed to install it in a virtual environment, but of you really want to you can install it outside a virtual environment. You just have to skip the virtualenv part.

### Install Dependencies

#### Debian, Ubuntu

```bash
sudo apt-get install python3 python3-pip ffmpeg
pip3 install --upgrade virtualenv
```

#### Fedora

```bash
sudo dnf install python3 python3-pip ffmpeg
pip3 install --upgrade virtualenv
```

### Install Kissenium

```bash
git clone git@github.com:AdiuvoDotFr/Kissenium.git kissenium
cd kissenium
python3 -m venv .

source bin/activate
pip3 install -r requirements.txt
```

Now Kissenium is installed on your system. To launch it, and the demo test if you do not have modified the tests, you have to type the following command :

```bash
python3 kissenium.py
```

Now, please refer to the [documentation page](documentation.html) to learn a little about how to work with Kissenium.