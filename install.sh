#!/usr/bin/bash

${PWD} = "$(pwd)"
$RED_PYTHON3_PACKAGE = "python3-pip"
$DEB_PYTHON3_PACKAGE = "python3-pip"
$RED_FFMPEG_PACKAGE = "ffmpeg"
$DEB_FFMPEG_PACKAGE = "ffmpeg"

SUDO=''
if (( $EUID != 0 )); then
    SUDO='sudo'
fi
${SUDO} a_command

# Test if ffmpeg is installed
if ! [ -x "$(command -v ffmpeg)"];then

	# Debian, Ubuntu, ...
    if [ -f /etc/debian_version ]; then
            ${SUDO} apt-get install -y ${DEB_FFMPEG_PACKAGE}
    # Redhat, Fedora
    elif [ -f /etc/redhat-release ]; then
            ${SUDO} dnf install -y ${RED_FFMPEG_PACKAGE}
    # Default
    else
            ${SUDO} apt-get install ${DEB_FFMPEG_PACKAGE}
    fi
fi

# Test if pip3 is installed
if ! [ -x "$(command -v pip3)"];then

	# Debian, Ubuntu, ...
    if [ -f /etc/debian_version ]; then
            ${SUDO} apt-get install -y ${DEB_PYTHON3_PACKAGE}
    # Redhat, Fedora
    elif [ -f /etc/redhat-release ]; then
            ${SUDO} dnf install -y ${FED_PYTHON3_PACKAGE}
    # Default
    else
            ${SUDO} apt-get install ${DEB_PYTHON3_PACKAGE}
    fi
fi

# Install or upgrade virtualenv
pip3 install --upgrade virtualenv
python3 -m venv .

source bin/activate
pip3 install -r requirements.txt
