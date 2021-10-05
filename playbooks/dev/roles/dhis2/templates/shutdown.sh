#!/bin/sh
export CATALINA_BASE="/home/{{test_dhis_user}}/{{test_dhis_user}}"
/home/{{test_dhis_user}}/{{test_dhis_user}}/bin/setenv.sh
/usr/share/tomcat9/bin/shutdown.sh
echo "Tomcat stopped"
