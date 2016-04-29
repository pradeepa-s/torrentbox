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

case "$1" in
  start)
    log_begin_msg "Starting deluged"
	sudo -u pi /usr/bin/deluged
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
