#!/bin/sh
export CATALINA_BASE="/home/{{dhis_user}}/{{dhis_user}}"
/home/{{dhis_user}}/{{dhis_user}}/bin/setenv.sh
/usr/share/tomcat9/bin/shutdown.sh
echo "Tomcat stopped"
