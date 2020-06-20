#!/bin/sh

echo "BIXOLON CO Ltd"
echo "BIXOLON CUPS DRIVER V1.3.5.1 Uninstaller"
echo "---------------------------------------"
echo ""
echo ""

ROOT_UID=0

if [ "$UID" -ne "$ROOT_UID" ]
then
    echo "This script requires root user access..."
    echo "Re-run as root user..."
    exit 1
fi

echo "Removing rastertoBixolon_* filter..."

 sudo rm -f /usr/bin/rastertoBixolon*
 sudo rm -f /usr/lib/cups/filter/rastertoBixolon*

echo ""

echo "Removing model ppd files... "
 sudo rm -rf /usr/share/cups/model/Bixolon
 sudo rm -rf /usr/share/ppd/Bixolon

echo ""
echo "Removing log files... "
 sudo rm -f /tmp/bixolonlogs
 sudo rm -f /tmp/bixolonlistp

echo ""
echo "Restarting CUPS"
    if [ -x /etc/software/init.d/cups ]
    then
        sudo /etc/software/init.d/cups stop
        sudo /etc/software/init.d/cups start
    elif [ -x /etc/rc.d/init.d/cups ]
    then
        sudo /etc/rc.d/init.d/cups stop
        sudo /etc/rc.d/init.d/cups start
    elif [ -x /etc/init.d/cups ]
    then
        sudo /etc/init.d/cups stop
        sudo /etc/init.d/cups start
    elif [ -x /sbin/init.d/cups ]
    then
        sudo /sbin/init.d/cups stop
        sudo /sbin/init.d/cups start
    elif [ -x /etc/software/init.d/cupsys ]
    then
        sudo /etc/software/init.d/cupsys stop
        sudo /etc/software/init.d/cupsys start
    elif [ -x /etc/rc.d/init.d/cupsys ]
    then
        sudo /etc/rc.d/init.d/cupsys stop
        sudo /etc/rc.d/init.d/cupsys start
    elif [ -x /etc/init.d/cupsys ]
    then
        sudo /etc/init.d/cupsys stop
        sudo /etc/init.d/cupsys start
    elif [ -x /sbin/init.d/cupsys ]
    then
        sudo /sbin/init.d/cupsys stop
        sudo /sbin/init.d/cupsys start
    else
        echo "Could not restart CUPS"
    fi
    sudo service cups stop
    sudo service cups start
    echo ""


echo "Uninstall Complete"
echo "Delete printer queue using OS tool, http://localhost:631, or http://127.0.0.1:631"
echo ""

