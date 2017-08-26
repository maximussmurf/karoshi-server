#!/bin/bash
#Copyright (C) 2007  Paul Sharrad

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
########################
#Required input variables
########################
#  _FIRSTNAME_
#  _SURNAME_
# _USERNAMESTYLE_
#  _PASSWORD1_  Password used for new user
#  _PASSWORD2_  Checked against PASSWORD1 for typos.
#  _GROUP_      This is the primary group for the new user eg yr2000, staff, officestaff.

#Detect mobile browser
MOBILE=no
source /opt/karoshi/web_controls/detect_mobile_browser
source /opt/karoshi/web_controls/version

##########################
#Language
##########################

STYLESHEET=defaultstyle.css
[ -f "/opt/karoshi/web_controls/user_prefs/$REMOTE_USER" ] && source "/opt/karoshi/web_controls/user_prefs/$REMOTE_USER"
export TEXTDOMAIN=karoshi-server

##########################
#Show page
##########################
echo "Content-type: text/html"
echo ""
echo '<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$"Add a New User"'</title><link rel="stylesheet" href="/css/'"$STYLESHEET"'?d='"$VERSION"'">'

if [ "$MOBILE" = yes ]
then
	echo '<link rel="stylesheet" type="text/css" href="/all/mobile_menu/sdmenu.css">
	<script src="/all/mobile_menu/sdmenu.js">
		/***********************************************
		* Slashdot Menu script- By DimX
		* Submitted to Dynamic Drive DHTML code library: www.dynamicdrive.com
		* Visit Dynamic Drive at www.dynamicdrive.com for full source code
		***********************************************/
	</script>
	<script>
	// <![CDATA[
	var myMenu;
	window.onload = function() {
		myMenu = new SDMenu("my_menu");
		myMenu.init();
	};
	// ]]>
	</script>'
fi

echo '</head><body><div id="pagecontainer">'
#########################
#Get data input
#########################
DATA=$(cat | tr -cd 'A-Za-z0-9\._:\-%*+-' | sed 's/*/%1123/g' | sed 's/____/QUADRUPLEUNDERSCORE/g' | sed 's/_/REPLACEUNDERSCORE/g' | sed 's/QUADRUPLEUNDERSCORE/_/g')
#########################
#Assign data to variables
#########################
END_POINT=23
function get_data {
COUNTER=2
DATAENTRY=""
while [[ $COUNTER -le $END_POINT ]]
do
	DATAHEADER=$(echo "$DATA" | cut -s -d'_' -f"$COUNTER")
	if [[ "$DATAHEADER" = "$DATANAME" ]]
	then
		let COUNTER="$COUNTER"+1
		DATAENTRY=$(echo "$DATA" | cut -s -d'_' -f"$COUNTER")
		break
	fi
	let COUNTER=$COUNTER+1
done
}

#Assign FIRSTNAME
DATANAME=FIRSTNAME
get_data
FIRSTNAME=$(echo "$DATAENTRY" | tr -cd 'A-Za-z0-9')

#Assign SURNAME
DATANAME=SURNAME
get_data
SURNAME=$(echo "$DATAENTRY" | tr -cd 'A-Za-z0-9')

#Assign ENROLLMENTNUMBER
DATANAME=ENROLLMENTNUMBER
get_data
ENROLLMENTNUMBER="$DATAENTRY"

#Assign password1
DATANAME=PASSWORD1
get_data
PASSWORD1="$DATAENTRY"

#Assign password2
DATANAME=PASSWORD2
get_data
PASSWORD2="$DATAENTRY"

#Assign group
DATANAME=GROUP
get_data
GROUP=$(echo "$DATAENTRY" | tr -cd 'A-Za-z0-9')

#Assign USERNAMESTYLE
DATANAME=USERNAMESTYLE
get_data
USERNAMESTYLE=$(echo "$DATAENTRY" | tr -cd 'A-Za-z0-9')

#Assign USERNAME
DATANAME=USERNAME
get_data
USERNAME=$(echo "$DATAENTRY" | tr -cd 'A-Za-z0-9' | tr '[:upper:]' '[:lower:]')

#Assign REQUESTFILE
DATANAME=REQUESTFILE
get_data
REQUESTFILE="$DATAENTRY"

#Assign NEXTLOGON
DATANAME=NEXTLOGON
get_data
NEXTLOGON="$DATAENTRY"

STARTCGI=add_user_fm.cgi
[ ! -z "$REQUESTFILE" ] && STARTCGI=request_new_users_fm.cgi

function show_status {
echo '<script>
alert("'"$MESSAGE"'");
window.location = "/cgi-bin/admin/'$STARTCGI'";
</script>'
[ "$MOBILE" = no ] && echo '</div>'
echo '</div></body></html>'
exit
}

function show_status2 {
echo '<script>
window.location = "/cgi-bin/admin/'$STARTCGI'";
</script>'
[ "$MOBILE" = no ] && echo '</div>'
echo '</div></body></html>'
exit
}


#Detect mobile browser
MOBILE=no
source /opt/karoshi/web_controls/detect_mobile_browser
source /opt/karoshi/web_controls/version

#Generate navigation bar
if [ $MOBILE = no ]
then
	DIV_ID=actionbox3
	#Generate navigation bar
	/opt/karoshi/web_controls/generate_navbar_admin
else
	DIV_ID=menubox
fi

#Show back button for mobiles
if [ "$MOBILE" = yes ]
then
	echo '<div style="float: center" id="my_menu" class="sdmenu">
	<div class="expanded">
	<span>'$"Add a New User"'</span>
<a href="/cgi-bin/admin/mobile_menu.cgi">'$"Menu"'</a>
</div></div><div id="mobileactionbox">
'
else
	echo '<div id="'$DIV_ID'"><div id="titlebox"><div class="sectiontitle">'$"Add a New User"'</div><br>'
fi

#########################
#Check https access
#########################
if [[ https_$HTTPS != https_on ]]
then
	export MESSAGE=$"You must access this page via https."
	show_status
fi
#########################
#Check user accessing this script
#########################
if [ ! -f /opt/karoshi/web_controls/web_access_admin ] || [ -z "$REMOTE_USER" ]
then
	MESSAGE=$"You must be a Karoshi Management User to complete this action."
	show_status
fi

if [[ $(grep -c ^"$REMOTE_USER": /opt/karoshi/web_controls/web_access_admin) != 1 ]]
then
	MESSAGE=$"You must be a Karoshi Management User to complete this action."
	show_status
fi
#########################
#Check data
#########################
#Check to see that firstname is not blank
if [ -z "$FIRSTNAME" ]
then
	MESSAGE=$"The firstname must not be blank."
	show_status
fi
#Check to see that surname is not blank
if [ -z "$SURNAME" ]
then
	MESSAGE=$"The surname must not be blank."
	show_status
fi

#Make sure first name and surname are capitalised
FIRSTNAME=$(echo $FIRSTNAME | tr '[:upper:]' '[:lower:]')
FIRST_CHAR=$(echo "${FIRSTNAME:0:1}" | tr '[:lower:]' '[:upper:]' )
FIRSTNAME="$FIRST_CHAR${FIRSTNAME:1}"

SURNAME=$(echo $SURNAME | tr '[:upper:]' '[:lower:]')
FIRST_CHAR=$(echo "${SURNAME:0:1}" | tr '[:lower:]' '[:upper:]' )
SURNAME="$FIRST_CHAR${SURNAME:1}"

SHOW_PASSWORD=no

if [ -z "$GROUP" ]
then
	MESSAGE=$"The group must not be blank."
	show_status
fi

#Check to see that password fields are not blank
if [ -z "$PASSWORD2" ] && [ ! -z "$PASSWORD1" ]
then
	MESSAGE=$"The password must not be blank."
	show_status
fi

if [ -z "$PASSWORD1" ]
then
	#Assume that a password needs to be randomly generated
	#Check password settings
	source /opt/karoshi/server_network/security/password_settings	

	if [ "$PASSWORDCOMPLEXITY" = on ]
	then
		PASSWORD1=$(openssl rand -base64 24 | head -c"$MINPASSWORDLENGTH" 2>/dev/null)
	else
		PASSWORD1=$(shuf -i 10000000000000-99999999999999 -n 1 | head -c"$MINPASSWORDLENGTH")
	fi
	SHOW_PASSWORD=yes
fi


if [ "$SHOW_PASSWORD" = no ]
then
	#Check that password has been entered correctly
	if [ "$PASSWORD1" != "$PASSWORD2" ]
	then
		MESSAGE=$"The passwords do not match."
		show_status
	fi
fi
#Check that usernamestyle is not blank
if [ -z "$USERNAMESTYLE" ]
then
	MESSAGE=$"The username style must not be blank."
	show_status
fi
#Check that usernamestyle is the correct value
if [ "$USERNAMESTYLE" != userstyleS1 ] && [ "$USERNAMESTYLE" != userstyleS2 ] && [ "$USERNAMESTYLE" != userstyleS3 ] && [ "$USERNAMESTYLE" != userstyleS4 ] && [ "$USERNAMESTYLE" != userstyleS5 ] && [ "$USERNAMESTYLE" != userstyleS6 ] && [ "$USERNAMESTYLE" != userstyleS7 ] && [ "$USERNAMESTYLE" != userstyleS8 ] && [ "$USERNAMESTYLE" != userstyleS9 ] && [ "$USERNAMESTYLE" != userstyleS10 ]
then
	MESSAGE=$"Incorrect username style."
	show_status
fi
#Check that username is not blank for style 10
if [ "$USERNAMESTYLE" = userstyleS10 ]
then
	if [ -z "$USERNAME" ]
	then
		MESSAGE=$"The username must not be blank."
		show_status	
	fi
fi

COUNTER=""
#Create username
DUPLICATECHECK=0

function check_username {
NAMESTATUS=ok
id -u "$USERNAME" 1>/dev/null 2>/dev/null
if [ "$?" = 0 ]
then
	NAMESTATUS=error
fi
getent group "$USERNAME" 1>/dev/null 2>/dev/null
if [ $? = 0 ]
then
	NAMESTATUS=error
fi
}

function create_username {
source /opt/karoshi/server_network/group_information/"$GROUP"
source /opt/karoshi/web_controls/version
if [ "$USERNAMESTYLE" = userstyleS1 ]
then
	USERNAME="${FIRSTNAME:0:1}$SURNAME$YEARSUFFIX$COUNTER"
fi
if [ "$USERNAMESTYLE" = userstyleS2 ]
then
	USERNAME="$YEARSUFFIX$COUNTER${FIRSTNAME:0:1}$SURNAME"
fi
if [ "$USERNAMESTYLE" = userstyleS3 ]
then
	USERNAME="$SURNAME${FIRSTNAME:0:1}$YEARSUFFIX$COUNTER"
fi
if [ "$USERNAMESTYLE" = userstyleS4 ]
then
	USERNAME="$FIRSTNAME.$SURNAME$YEARSUFFIX$COUNTER"
fi
if [ "$USERNAMESTYLE" = userstyleS5 ]
then
	USERNAME="$SURNAME.$FIRSTNAME$YEARSUFFIX$COUNTER"
fi
if [ "$USERNAMESTYLE" = userstyleS6 ]
then
	USERNAME="$YEARSUFFIX$COUNTER$SURNAME${FIRSTNAME:0:1}"
fi
if [ "$USERNAMESTYLE" = userstyleS7 ]
then
	USERNAME="$YEARSUFFIX$COUNTER$FIRSTNAME${SURNAME:0:1}"
fi
if [ "$USERNAMESTYLE" = userstyleS8 ]
then
	[ -z "$COUNTER" ] && COUNTER=1
	USERNAME="$FIRSTNAME${SURNAME:0:$COUNTER}"
fi
if [ "$USERNAMESTYLE" = userstyleS9 ]
then
#Check to see that enrolment is not blank
	if [ -z "$ENROLLMENTNUMBER" ]
	then
		MESSAGE=$"The enrolment number must not be blank."
		show_status
	fi
	[ -z "$COUNTER" ] && COUNTER=1
	if [ "$DUPLICATECHECK" = 0 ]
	then
		USERNAME="$ENROLLMENTNUMBER"
	else
		USERNAME="$ENROLLMENTNUMBER.$COUNTER"
	fi
fi

if [ "$USERNAMESTYLE" = userstyleS10 ]
then
	[ -z "$COUNTER" ] && COUNTER=1
	USERNAME="$USERNAME$COUNTER"
fi

USERNAME=$(echo "$USERNAME" | tr '[:upper:]' '[:lower:]')
}

[ -z "$USERNAME" ] && create_username

#Correct new username if user already exists.
INITUSERNAME=$USERNAME
DUPLICATECHECK=1
ACTIONUSER=0

if [ "$USERNAMESTYLE" != userstyleS8 ]
then
	while [ "$DUPLICATECHECK" = 1 ]
	do
		check_username
		if [ "$NAMESTATUS" = error ]
		then
			[ -z "$COUNTER" ] && COUNTER=1
			#user exists
			create_username
			let COUNTER=$COUNTER+1
			ACTIONUSER=1
		else
			DUPLICATECHECK=0
		fi
	done
fi

if [ "$USERNAMESTYLE" = userstyleS8 ]
then
	while [ $DUPLICATECHECK = 1 ]
	do
		check_username
		if [ $NAMESTATUS = error ]
		then
			#user exists
			let COUNTER=$COUNTER+1
			create_username
			ACTIONUSER=1
		else
			DUPLICATECHECK=0
		fi
	done
fi

#Check password settings
source /opt/karoshi/server_network/security/password_settings

#Convert special characters back for new password to check password strength
NEW_PASSWORD=$(echo "$PASSWORD1" | sed 's/+/ /g; s/%21/!/g; s/%3F/?/g; s/%2C/,/g; s/%3A/:/g; s/%7E/~/g; s/%40/@/g; s/%23/#/g; s/%24/$/g; s/%26/\&/g; s/%2B/+/g; s/%3D/=/g; s/%28/(/g; s/%29/)/g; s/%5E/^/g; s/%7B/{/g; s/%7D/}/g; s/%3C/</g; s/%3E/>/g; s/%5B/[/g; s/%5D/]/g; s/%7C/|/g; s/%22/"/g; s/%1123/*/g' | sed "s/%27/'/g" | sed 's/%3B/;/g' | sed 's/%60/\`/g' | sed 's/%5C/\\/g' | sed 's/%2F/\//g' | sed 's/%25/%/g')

PASSLENGTH=${#NEW_PASSWORD}

#Check to see that password has the required number of characters
if [ "$PASSLENGTH" -lt "$MINPASSLENGTH" ]
then
	MESSAGE=''$"Username"': '$USERNAME'\n'$"Password length"': '$PASSLENGTH'\n'$"Required password length"': '$MINPASSLENGTH''
	show_status
fi

if [ "$PASSWORDCOMPLEXITY" = on ]
then
	CASECHECK=ok
	CHARCHECK=ok

	#Check that the password has a combination of characters and numbers
	if [[ $(echo "$PASSWORD1"'1' | tr -cd '0-9\n') = 1 ]]
	then
		CHARCHECK=fail
	fi
	if [[ $(echo "$PASSWORD1"'A' | tr -cd 'A-Za-z\n') = A ]]
	then
		CHARCHECK=fail
	fi

	if [[ $(echo "$PASSWORD1"'A' | tr -cd 'A-Z\n') = A ]]
	then
		CASECHECK=fail
	fi
	if [[ $(echo "$PASSWORD1"'a' | tr -cd 'a-z\n') = a ]]
	then
		CASECHECK=fail
	fi

	if [ "$CASECHECK" = fail ] || [ "$CHARCHECK" = fail ]
	then
		MESSAGE=$"A combination of upper and lower case characters and numbers is required."
		show_status
	fi
fi

#Prompt to create user with revised username if username existed or create user.
if [ "$ACTIONUSER" = 1 ]
then
	echo '<form action="/cgi-bin/admin/add_user.cgi" method="post">
	<input name="____FIRSTNAME____" value="'"$FIRSTNAME"'" type="hidden">
	<input name="____SURNAME____" value="'"$SURNAME"'" type="hidden">
	<input name="____PASSWORD1____" value="'"$PASSWORD1"'" type="hidden">
	<input name="____PASSWORD2____" value="'"$PASSWORD2"'" type="hidden">
	<input name="____GROUP____" value="'"$GROUP"'" type="hidden">
	<input name="____USERNAMESTYLE____" value="'"$USERNAMESTYLE"'" type="hidden">
	<input name="____USERNAME____" value="'"$USERNAME"'" type="hidden">
	<input name="____ENROLLMENTNUMBER____" value="'"$ENROLLMENTNUMBER"'" type="hidden">
	'"$INITUSERNAME"' - '$"This user already exists."'<br><br>'$"Create user"' '"$USERNAME"'?<br><br>
	<input value="'$"Submit"'" class="button" type="submit">
	</form></div></div></body></html>'
	exit
else
	MD5SUM=$(md5sum /var/www/cgi-bin_karoshi/admin/add_user.cgi | cut -d' ' -f1)
	#Add user
	echo "$REMOTE_USER:$REMOTE_ADDR:$MD5SUM:$FIRSTNAME:$SURNAME:$USERNAME:$PASSWORD1:$GROUP:$USERNAMESTYLE:$ENROLLMENTNUMBER:$REQUESTFILE::$NEXTLOGON:" | sudo -H /opt/karoshi/web_controls/exec/add_user
EXEC_STATUS="$?"
	MESSAGE=''$"Forename":' '"${FIRSTNAME^}"'\n'$"Surname"': '"${SURNAME^}"'\n'$"Username"': '"$USERNAME"'\n'$"Created with primary group"' '"$GROUP"'.'
	if [ "$EXEC_STATUS" = 101 ]
	then
		MESSAGE=''$"There was a problem with this action."' '$"Please check the karoshi web administration logs for more details."''
		show_status
	fi

	if [ "$EXEC_STATUS" = 103 ]
	then
		MESSAGE=''"$MESSAGE"' '$"The enrolment number entered is already in use and has been left blank for this user."''
		show_status
	fi

	if [ "$EXEC_STATUS" = 105 ]
	then
		MESSAGE=''$"A server required for this action was offline."' '$"Please check the karoshi web administration logs for more details."''
		show_status
	fi

	if [ "$EXEC_STATUS" -eq 106 ]
	then
		MESSAGE=''"$USERNAME"' - '$"A group with the same name as this user already exists, not creating user"''
		show_status
	fi

	echo '
	<ul><li>'$"User created"'</li></ul>
	<ul><li>'$"Forename"': '"${FIRSTNAME^}"'</li></ul>
	<ul><li>'$"Surname"': '"${SURNAME^}"'</li></ul>
	<ul><li>'$"Username"': '"$USERNAME"'</li></ul>
	<ul><li>'$"Primary Group"': '"$GROUP"'</li></ul>	
	'
	if [ "$SHOW_PASSWORD" = yes ]
	then
		MESSAGE=''"$MESSAGE"'\n\n'$"Password"': '"$PASSWORD1"''
	fi
	sleep 5
	show_status2
fi
exit
