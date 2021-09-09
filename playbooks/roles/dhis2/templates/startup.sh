#!/bin/sh
set -e

if [[ `id -nu` != "{{dhis_user}}" ]];then
   echo "Not running as {{dhis_user}}, exiting.."
   exit 1
fi

/home/{{dhis_user}}/{{dhis_user}}/bin/setenv.sh

export CATALINA_BASE="/home/{{dhis_user}}/{{dhis_user}}"
/usr/share/tomcat9/bin/startup.sh
echo "Tomcat started"