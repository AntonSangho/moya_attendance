#!/bin/sh

echo "BIXOLON CO Ltd"
echo "BIXOLON CUPS DRIVER V1.3.5.1 Installer"
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

echo "Copying rastertoBixolon_v1.3.5.1 filter..."


 sudo chmod +x rastertoBixolon_v1.3.5.1
 sudo cp ./rastertoBixolon_v1.3.5.1 /usr/bin/
 sudo chmod 0755 /usr/bin/rastertoBixolon_v1.3.5.1
echo ""

echo "Creating Symbolic Link...."
  sudo ln -s /usr/bin/rastertoBixolon_v1.3.5.1 /usr/lib/cups/filter/rastertoBixolon
  sudo chmod 0755 /usr/lib/cups/filter/rastertoBixolon
echo ""


if [ -x /etc/init.d/cupsys ]
then
	if [ -r /etc/debian_version ]
	then
		if [ -r /etc/lsb-release ]
		then
			 sudo cp -r ./Bixolon /usr/share/cups/model/
			 sudo chmod 0755 /usr/share/cups/model/Bixolon/*
		else
			 sudo cp ./Bixolon /usr/share/ppd/ 
			 sudo chmod 0755 /usr/share/ppd/Bixolon/*
			 
		fi
	else
		 sudo cp -r ./Bixolon /usr/share/cups/model/
		 sudo chmod 0755 /usr/share/cups/model/Bixolon/*
		 
	fi
else
	if [ -r /etc/debian_version ]
	then
		 sudo cp -r ./Bixolon /usr/share/cups/model/
		 sudo chmod 0755 /usr/share/cups/model/Bixolon/*
		
	else
		 sudo cp -r ./Bixolon /usr/share/cups/model/
		 sudo chmod 0755 /usr/share/cups/model/Bixolon/*
		
	fi
fi 
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


echo "Install Complete"
echo "Add printer queue using OS tool, http://localhost:631, or http://127.0.0.1:631"
echo ""

