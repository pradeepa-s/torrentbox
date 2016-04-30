#! /bin/sh
### BEGIN INIT INFO
# Provides:          torrentbox
# Required-Start:    $all
# Required-Stop:     
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start deluged and torrentbox
### END INIT INFO

PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/bin

. /lib/init/vars.sh
. /lib/lsb/init-functions
# If you need to source some other scripts, do it here

# Set the username
USER_NAME=pi

# Python script location
TORRBOX_LOC=/home/pi/torrent_box

case "$1" in
  start)
    log_begin_msg "Starting deluged"
	sudo -u $USER_NAME /usr/bin/deluged
	sudo start-stop-daemon --start --background --pidfile /var/run/torrentbox.pid --make-pidfile --user $USER_NAME --chuid $USER_NAME --startas $TORRBOX_LOC/torrentbox.py
    log_end_msg $?
    exit 0
    ;;
  stop)
    log_begin_msg "Stopping deluged"
    	sudo pkill deluged
    log_end_msg $?
    exit 0
    ;;
  *)
    echo "Usage: /etc/init.d/<your script> {start|stop}"
    exit 1
    ;;
esac
