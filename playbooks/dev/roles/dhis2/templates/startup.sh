#!/bin/sh
set -e

if [[ `id -nu` != "{{test_dhis_user}}" ]];then
   echo "Not running as {{test_dhis_user}}, exiting.."
   exit 1
fi

/home/{{test_dhis_user}}/{{test_dhis_user}}/bin/setenv.sh

export CATALINA_BASE="/home/{{test_dhis_user}}/{{test_dhis_user}}"
/usr/share/tomcat9/bin/startup.sh
echo "Tomcat started"