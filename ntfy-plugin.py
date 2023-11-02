#!/usr/bin/env python3
# ntfy.sh plugin
# Bulk: no
#
# Sends notifications to mobile phones (iOS and Android) using the ntfy.sh service 
# For details, please check https://ntfy.sh
# Install the ntfy app on iOS and Android on your phone
# 
# Checkmk usage
# Select the 'ntfy-plugin' as notification plugin
# Parameter 1 (mandatory): Provide a unique topic, which you also need to add in the app
# Parameter 2 (optional): Provide an access token in the format 'Bearer tk_AgQdq7mVBoFD37zQVN29RhuMzNIz2'
#
# Some additional noteworthy comments
# - In FREE mode, you can send only 250 messages per day. Sufficient for home usage or testing, but get an account if you are a company.
# - To reserve a topic exclusively for you, you need an account. For testing or home usage, just select a topic, which is unique
# - For testing, the plugin can be used without an access token
# - Error messages are written to ~/var/log/notify.log. In case of any issue, please have a look there
# - This is my first Python program. Please look at the code with clemency. I used VC Code with Pydantic (type checking mode: Basic) and Black

import os
import sys
import requests
import json


# === Definitions ===
# ntfy Server - Change if you want to use another server. See https://docs.ntfy.sh/integrations/#alternative-ntfy-servers
ntfy_server = "ntfy.sh"     # Offical server
# ntfy_server = "ntfy.tedomum.net"      # France 1
# ntfy_server = "ntfy.hostux.net"       # France 2
# ntfy_server = "ntfy.adminforge.de"    # Germany 1
# ntfy_server = "ntfy.envs.net"         # Germany 2
# ntfy_server = "ntfy.mtze.de"          # Germany 3
# ntfy_server = "ntfy.jea.fi"           # Finland
# Self installed servers can be added as well

# === Tags to Icons ===
# Please check this page for all available icons: https://docs.ntfy.sh/emojis/
tag_warn = "yellow_circle"
tag_critdown = "red_circle"
tag_okup = "green_circle"
tag_unkn = "white_circle"


# Get topic and access token from the environment variables
def GetPluginParams():
	env_vars = os.environ

	topic = str(env_vars.get("NOTIFY_PARAMETER_1"))
	access_token = str(env_vars.get("NOTIFY_PARAMETER_2"))

	# "None", if not in the environment variables
	if (topic == "None"):
		print("Mandatory first parameter is missing: ntfy topic")
		return 2, "", "" # do not return anything, create final error
	
	if access_token == "None":   # Empty the access_token for later usage
		access_token = ""

	if ((access_token != "") and (access_token.startswith('Bearer') == False)):
		print(f"Optional second parameter ntfy access token must start with Bearer:{access_token}")
		return 2, "", ""  # do not return anything, create final error
	
	return 0, topic, access_token
	

# Get the content of the message from the environment variables
def GetNotificationDetails():
	env_vars = os.environ
	what = env_vars.get("NOTIFY_WHAT")

	# Get the right state
	if what == "SERVICE":
		state = env_vars.get("NOTIFY_SERVICESHORTSTATE")
	else:
		state = env_vars.get("NOTIFY_HOSTSHORTSTATE")

	# Set prio and tags
	match state:
		case "OK":
			prio = 3
			tag_icon = tag_okup
		case "UP":
			prio = 3
			tag_icon = tag_okup
		case "WARN":
			prio = 4
			tag_icon = tag_warn
		case "CRIT":
			prio = 5
			tag_icon = tag_critdown
		case "DOWN":
			prio = 5
			tag_icon = tag_critdown
		case "UNKN":
			prio = 2
			tag_icon = tag_unkn
		case _:
			prio = 0
			tag_icon = "ERROR_UNKNOWN_STATE" # this text will show up in the tags section of the app
			pass

	# Get remaining common notification details
	shortdatetime = env_vars.get("NOTIFY_SHORTDATETIME")
	omd_site = env_vars.get("OMD_SITE")

	tag_datetime = f'{shortdatetime}'
	tag_site = f'Site: {omd_site}'

	hostalias = env_vars.get("NOTIFY_HOSTALIAS")
	notificationtype = env_vars.get("NOTIFY_NOTIFICATIONTYPE")
	host_addr_4 = env_vars.get("NOTIFY_HOST_ADDRESS_4")

	# Build title and message
	if what == "SERVICE":
		servicedesc = env_vars.get("NOTIFY_SERVICEDESC")
		serviceoutput = env_vars.get("NOTIFY_SERVICEOUTPUT")
		
		title = f'{servicedesc} on {hostalias}'
		message = f'{what}: {notificationtype} on {hostalias}({host_addr_4})\n{serviceoutput}'
	else:
		hostoutput = env_vars.get("NOTIFY_HOSTOUTPUT")

		title = f'{hostalias}({host_addr_4})'
		message = f'{what}: {notificationtype}\n{hostoutput}'

	return prio, tag_icon, title, message, tag_datetime, tag_site


# Send the message via ntfy.sh
def SendNtfyPush(topic, access_token, prio, tag_icon, title, message, tag_datetime, tag_site):
	data = json.dumps({
		"topic": topic,
		"message": message,
		"title": title,
		"tags": [tag_icon,tag_datetime, tag_site],
		"priority": prio
	})

	if access_token != "":
		response = requests.post("https://"+ntfy_server, 
						   data,
						   headers={"Authorization": access_token
						})
	else:
		response = requests.post("https://"+ntfy_server, data)
		
	if response.status_code == 200: # Sending was successful
		return 0
	else:
		print(f'ntfy server request returns http error code:{response.status_code}')
		return 2
	

def main():
	return_code, topic, access_token = GetPluginParams()

	if return_code != 0:
		return return_code   # Abort, if parameter for topic is missing

	prio, tag_icon, title, message, tag_datetime, tag_site = GetNotificationDetails()

	return_code = SendNtfyPush(topic, access_token, prio, tag_icon, title, message, tag_datetime, tag_site)

	return return_code


if __name__ == '__main__':
	sys.exit(main())

