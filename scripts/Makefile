export DISPLAY=:0
RS232_PORT=/dev/pts/4

start:
	xset s off -dpms # disable dpms and screensaver
	xset s off # disable screensaver
	xrandr --output HDMI-1 --rotate right # rotate screen to the right direction
	gnome-terminal --full-screen -- /usr/bin/python ../obd-server/tui2.py --rs232_port $(RS232_PORT)

install:
	pip install -r ../requirements.txt
	-mkdir -p ~/.config/autostart/
	echo "[Desktop Entry]" > ~/.config/autostart/obdb.desktop
	echo "Type=Application" >> ~/.config/autostart/obdb.desktop
	echo "Exec=\"$(shell pwd)/start.sh\"" >> ~/.config/autostart/obdb.desktop
	echo "Name=obdb" >> ~/.config/autostart/obdb.desktop
	echo "Comment=Autostart obdb at login" >> ~/.config/autostart/obdb.desktop
