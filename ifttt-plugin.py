#!/usr/bin/env python3
# IFTTT plugin
# Bulk: no
#
# Sends notifications to IFTTT.com (If This, Then That) for all types of automation
# See https://www.ifttt.com for details
#  
# Checkmk usage
# Select the 'ifttt-plugin' as the notification plugin
#  Parameter 1 (mandatory): The event name defined for the webhook, e.g. 'cmk_notification'
#  Parameter 2 (mandatory): Your personal IFTTT account key, e.g. '0_1ft9AyL1zB2Lx3sC456'
# 
# Some additional noteworthy comments
# - You can find your IFTTT key here: My Services > Webhooks > Settings
# - Error messages will be written to ~/var/log/notify.log. Please take a look there if you encounter any problems.
# - implemented with VC Code using Pydantic (type checking mode: Basic) and Black


import os
import sys
import requests
import json


# Get IFTTT WebHookURL from the environment variables and validate it
def GetPluginParams():
	env_vars = os.environ

	event_name = str(env_vars.get("NOTIFY_PARAMETER_1"))
	ifttt_key = str(env_vars.get("NOTIFY_PARAMETER_2"))

	# "None", if event_name is not in the environment variables
	if (event_name == "None"):
		print("ifttt-plugin: Mandatory first parameter is missing: Event name")
		return 2, "" 	# do not return anything, create final error
	
	# "None", if ifttt_key is not in the environment variables
	if (ifttt_key == "None"):
		print("ifttt-plugin: Mandatory second parameter is missing: IFTTT webhook key")
		return 2, "" 	# do not return anything, create final error

	# Build correct URL
	WebHookURL = f"https://maker.ifttt.com/trigger/{event_name}/json/with/key/{ifttt_key}"

	return 0, WebHookURL
	

# Get the content of the message from the environment variables
def GetNotificationDetails():
	env_vars = os.environ
	
	what = env_vars.get("NOTIFY_WHAT")

	# Handy hosts or service differently
	if what == "SERVICE":
		state = env_vars.get("NOTIFY_SERVICESHORTSTATE")
	else:
		state = env_vars.get("NOTIFY_HOSTSHORTSTATE")

	# Build high level title and message
	hostalias = env_vars.get("NOTIFY_HOSTALIAS")
	notificationtype = env_vars.get("NOTIFY_NOTIFICATIONTYPE")
	host_addr_4 = env_vars.get("NOTIFY_HOST_ADDRESS_4")
	if what == "SERVICE":
		servicedesc = env_vars.get("NOTIFY_SERVICEDESC")
		serviceoutput = env_vars.get("NOTIFY_SERVICEOUTPUT")
		
		title = f'{servicedesc} on {hostalias}'
		message = f'{what}: {notificationtype} on {hostalias}({host_addr_4})\n{serviceoutput}'
	else:
		hostoutput = env_vars.get("NOTIFY_HOSTOUTPUT")

		title = f'{hostalias}({host_addr_4})'
		message = f'{what}: {notificationtype}\n{hostoutput}'
	
	# Fill the dictionary with the high level notification data
	data = {
            'state': state,
			'service-or-host': what,
			'title': title,
			'message': message
        }

	# Add remaining data copied 1:1 from the notification
	for key, value in env_vars.items():
		if "NOTIFY_" in key:
			match key:
				case "NOTIFY_PARAMETER_1": # Filter our the WebHookURL secret
					pass
				case _:
					data[key] = value


	return data


# Send the message to IFTTT
def StartIftttApplet(WebHookURL, data):
	return_code = 0

    # Set header information
	headers = {
        'Content-Type': 'application/json'
    }

	try:
        # Make the POST request to start the workflow
		response = requests.post(WebHookURL, headers=headers, data=json.dumps(data))

        # Check the response status code
		if response.status_code == 200:
			print(f"ifttt-plugin: Workflow started successfully.")
		else:
			print(f"ifttt-plugin: Failed to start the workflow. Status code: {response.status_code}")
			print(response.text)
			return_code = 2

	except Exception as e:
		print(f"ifttt-plugin: An error occurred: {e}")
		return_code = 2

	return return_code	

	

def main():
	return_code, WebHookURL = GetPluginParams()

	if return_code != 0:
		return return_code   # Abort, if parameter for the webhook is missing

	data = GetNotificationDetails()

	return_code = StartIftttApplet(WebHookURL, data)

	return return_code


if __name__ == '__main__':
	sys.exit(main())

