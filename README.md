# kiosk
dtoverlay=pi3-disable-wifi
dtoverlay=pi3-disable-bt
sudo apt install exfat-fuse
sudo apt-get install cups cups-bsd libcups2-dev gcc
sudo cupsctl --remote-admin --remote-any
sudo usermod -a -G lpadmin pi
sudo usermod -a -G watchdog pi
service cups restart
sudo apt-get install python3-pip
sudo pip3 install pycups
sudo pip3 install pycurl
sudo pip3 install pyserial
pip install RPi.GPIO
sudo nano /etc/udev/rules.d/60-watchdog.rules
>KERNEL=="watchdog", MODE="0660", GROUP="watchdog"
