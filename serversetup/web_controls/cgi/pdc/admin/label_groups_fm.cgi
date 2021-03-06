#!/bin/bash
#Copyright (C) 2008  Paul Sharrad

#This file is part of Karoshi Server.
#
#Karoshi Server is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Karoshi Server is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.
#
#You should have received a copy of the GNU Affero General Public License
#along with Karoshi Server.  If not, see <http://www.gnu.org/licenses/>.

#
#The Karoshi Team can be contacted at: 
#mpsharrad@karoshi.org.uk
#jsharrad@karoshi.org.uk

#
#Website: http://www.karoshi.org.uk
############################
#Language
############################

STYLESHEET=defaultstyle.css
TIMEOUT=300
NOTIMEOUT=127.0.0.1
[ -f /opt/karoshi/web_controls/user_prefs/"$REMOTE_USER" ] && source /opt/karoshi/web_controls/user_prefs/"$REMOTE_USER"
export TEXTDOMAIN=karoshi-server

source /opt/karoshi/web_controls/group_dropdown_def
source /opt/karoshi/web_controls/version
#Check if timout should be disabled
if [[ $(echo "$REMOTE_ADDR" | grep -c "$NOTIMEOUT") = 1 ]]
then
	TIMEOUT=86400
fi

############################
#Show page
############################
echo "Content-type: text/html"
echo ""
echo '
<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>'$"Label Groups"'</title><meta http-equiv="REFRESH" content="'"$TIMEOUT"'; URL=/cgi-bin/admin/logout.cgi">
<link rel="stylesheet" href="/css/'"$STYLESHEET"'?d='"$VERSION"'">
<script src="/all/stuHover.js" type="text/javascript"></script>
</head>
<body onLoad="start()"><div id="pagecontainer">'
#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin

WIDTH=100
ICON1=/images/submenus/user/groups.png

echo '<form action="/cgi-bin/admin/label_groups.cgi" method="post"><div id="actionbox3"><div id="titlebox">

<div class="sectiontitle">'$"Label Groups"' <a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Group_Management#Labelling_groups"><img class="images" alt="" src="/images/help/info.png"><span>'$"This will let you add labels to your groups. The labels are shown to help you choose the correct group when adding new users to the system."'</span></a></div>
<table class="tablesorter"><tbody><tr>

	<td style="vertical-align: top; height: 30px; white-space: nowrap; min-width: '"$WIDTH"'px; text-align:center;">
		<button class="info infonavbutton" formaction="groups.cgi" name="_ViewNewPasswords_" value="_">
			<img src="'"$ICON1"'" alt="'$"Group Management"'">
			<span>'$"Manage groups."'</span><br>
			'$"Group Management"'
		</button>
	</td>

</tr></tbody></table>
<br>

</div><div id="infobox">'

#groups
COUNTER=1
echo '<table class="tablesorter" style="text-align: left;" ><thead><tr><th style="width: 200px;">'$"Group"'</th><th style="width: 100px;">'$"Label"'</th><th style="width: 60px;"></th><th style="width: 200px;">'$"Group"'</th><th style="width: 100px;">'$"Label"'</th><th style="width: 60px;"></th></tr></thead><tbody><tr>'
for GROUPNAMES in /opt/karoshi/server_network/group_information/*
do
	GROUPNAME=$(basename "$GROUPNAMES")
	GROUPNAME2=$(echo "$GROUPNAME" | sed 's/-/HYPHEN/g')
	UPPERGROUPNAME="${GROUPNAME2^^}"
	LABEL="${!UPPERGROUPNAME}"
	echo '<td>'"$GROUPNAME"'</td><td><input maxlength="20" size="20" name="____'"$UPPERGROUPNAME"':" value="'"$LABEL"'"></td><td style="width: 60px;"></td>'

	if [ $COUNTER = 2 ]
	then
		echo "</tr><tr>"
		COUNTER=0
	fi
	let COUNTER="$COUNTER"+1
done
echo '</tbody></table><br>
<input value="'$"Submit"'" class="button" type="submit"> <input value="'$"Reset"'" class="button" type="reset">
</div>
</div>
</form>
</div></body>
</html>
'
exit

