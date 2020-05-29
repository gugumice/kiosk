# kiosk
#Disable WiFi & BT
echo "dtoverlay=pi3-disable-wifi" | sudo tee -a /boot/config.txt
echo "dtoverlay=pi3-disable-bt" | sudo tee -a /boot/config.txt

sudo apt install exfat-fuse
sudo apt-get install cups cups-bsd libcups2-dev gcc
sudo usermod -a -G lpadmin pi
sudo cupsctl --remote-admin --remote-any
sudo service cups restart
sudo apt-get install python3-pip
sudo pip3 install pycups
sudo pip3 install pycurl
sudo pip3 install pyserial
#sudo apt install python3-rpi.gpio
sudo apt install python3-gpiozero
#pip install RPi.GPIO
#Set permissions for watchdog
sudo nano /etc/udev/rules.d/60-watchdog.rules
KERNEL=="watchdog", MODE="0660", GROUP="watchdog"
sudo reboot
sudo usermod -a -G watchdog pi
