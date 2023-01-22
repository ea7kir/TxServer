# Installing TxServer

LATEST INSTALL METHOD on Bullseye 64-bit Lite

TODO: add instructions to burn Bullseye to micro sd card.

## BEGIN

\$ cd

\$ sudo apt update

\$ sudo apt full-upgrade -y

\$ sudo apt autoremove

\$ sudo rpi-eeprom-update -a

	and proceed as neccessary

\$ sudo reboot

## INSTAL GIT

\$ sudo apt install git -y

SEE: https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup

\$ git config --global user.name "ea7kir"
\$ git config --global user.email "mikenaylorspain@icloud.com"
\$ git config --global init.defaultBranch main

## INSTALL PYENV

\$ sudo apt-get update

\$ sudo apt-get install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

\$ git clone https://github.com/pyenv/pyenv.git ~/.pyenv

\$ echo 'export PYENV_ROOT="\$HOME/.pyenv"' >> ~/.bashrc

\$ echo 'export PATH="\$PYENV_ROOT/bin:\$PATH"' >> ~/.bashrc

\$ echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "\$(pyenv init --path)"\nfi' >> ~/.bashrc

\$ exec \$SHELL

## INSTALL PYTHON

\$ sudo apt install wget build-essential libreadline-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev -y

\$ pyenv global system

\$ pyenv versions

	* system (set by /home/pi/.pyenv/version)

\$ pyenv install 3.11.1

\$ pyenv versions

	* system (set by /home/pi/.pyenv/version)
	3.11.1

\$ pyenv global 3.11.1

	* system 3.11.1 (set by /home/pi/.pyenv/version)
	3.9.2

## UPGRADE PIP

\$ pip install --upgrade pip

## INSTALL WEBSOCKETS & PyYAML

\$ pip install websockets PyYAML

## INSTALL PIGPIO (for RELAYS & SENSORS)

PERHAPS THIS SHOULD BE INSTALLED BEFORE PYTHON 3.11.1

\$ sudo apt install pigpio python-pigpio python3-pigpio

\$ sudo systemctl enable pigpiod

\$ sudo systemctl start pigpiod

## SAT NOTES -

\$ sudo systemctl stop TxRoof

sudo systemctl status TxRoof

\$ sudo systemctl enable TxRoof

\$ sudo systemctl disable TxRoof

SAT NOTES - FOR I2C

\$ sudo i2cdetect -y 1

EDITED /boot/config.txt to:

From: dtparam=i2c_arm=on
To:   dtparam=i2c_arm=on,i2c_arm_baudrate=50000
Or:   100000, 400000, 1000000

Configuring two I2C buses
dtoverlay=i2c1,pins_2_3   (board pins  3,  5)
dtoverlay=i2c3,pins_4_5   (board pins  7, 29)

dtoverlay=i2c4,pins_6_7   (board pins 31, 26)
dtoverlay=i2c5,pins_12_13 (board pins 32, 33)
dtoverlay=i2c6,pins_22_23 (board pins 15, 16)

## Clone my repo in VSCODE
