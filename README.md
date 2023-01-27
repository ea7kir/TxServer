# TxServer

Control a DATV Preamp and Power Amplifier remotely from the shack using TxTouch.

## Hardware

- Raspberry Pi 4B with 4GB RAM
- Relays
- Temperature Sensors
- Fans

**A keyboard and mouse are not required for normal use.**

## Installing

On a Mac or Windows PC, install and launch the **Raspberry Pi Imager**.

- Click **CHOOSE OS** and select **Raspberry Pi OS Lite (64-bit)**
- Click the **WHEEL** bottom right
    - Select hostname to **txserver**
    - Select Enable SSH to **Use password autentication**
    - Select Set username and password to **pi* and choose your own password
    - Clcik **SAVE**
- Insert a fast 32GB Micro SD Card
- Click **CHOOSE STORAGE** and select your SSD Card
- Click **WRITE**

Remove the SSD card, insert it into the Raspberry Pi, and apply power.  The Pi will reboot during the install process, so wait.

From your Mac or Windows PC, open a terminal and login to the Pi.

    - ssh pi@txserver.local and enter your password.
