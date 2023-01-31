#!/bin/bash

# to copy this file from Mac to Rpi, type
# scp install_3.sh pi@txserver.local/install_3.sh

echo "Installing TxServer Part 3"

echo
echo "-------------------------------"
echo "-- Installing Python 3.11.1"
echo "--"
echo "-- this will take some time..."
echo "-------------------------------"
echo

pyenv install 3.11.1

echo
echo "-------------------------------"
echo "-- Setting env to Python 3.11.1"
echo "-------------------------------"
echo

pyenv global 3.11.1
pyenv versions

echo
echo "-------------------------------"
echo "-- Updrading PIP"
echo "-------------------------------"
echo

pip install --upgrade pip

echo
echo "-------------------------------"
echo "-- Install pigio & enable"
echo "-------------------------------"
echo

sudo apt install pigpio python-pigpio python3-pigpio
sudo systemctl enable pigpiod
sudo systemctl start pigpiod

echo
echo "-------------------------------"
echo "-- Installing pigpio, websockets & PyYAML"
echo "-------------------------------"
echo

pip install pigpio websockets PyYAML

echo
echo "-------------------------------"
echo "-- Enable 1-Wire and I2C"
echo "-------------------------------"
echo

echo "THIS IS NOT WORKING YET"

echo
echo "-------------------------------"
echo "-- Cloning TxServer from github"
echo "-------------------------------"
echo

echo "THIS IS NOT WORKING YET"
# git clone https://github.com/ea7kir/RxServer.git

echo
echo "-------------------------------"
echo "-- Done"
echo "-------------------------------"
echo

echo "Clone from VSCODE"
