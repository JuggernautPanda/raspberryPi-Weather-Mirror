# raspberryPi-Weather-Mirror
To make browser started automatically:
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
@xset s off
@xset -dpms
@xset s noblank
@chromium-browser --kiosk http://localhost:5000

LCD display
git clone https://github.com/goodtft/LCD-show.git
The templates and static folder contents got swapped.
