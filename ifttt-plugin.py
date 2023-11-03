#!/usr/bin/env python3
# IFTTT plugin
# Bulk: no
#
# Sends notifications to IFTTT.Com (If This, Than That) for all types of automation
# For details, please check https://www.ifttt.com
#  
# Checkmk usage
# Select the 'ifttt-plugin' as the notification plugin
#  TBD Parameter 1 (mandatory): Provide the webhook URL copied from a webhook task in IFTTT that is the starting point for your workflow
# 
# Some additional noteworthy comments
# - xxxx
# - Error messages are written to ~/var/log/notify.log. Please take a look there if you encounter any problems.
# - implemented with VC Code using Pydantic (type checking mode: Basic) and Black


import os
import sys
import requests
import json


# Get IFTTT WebHookURL from the environment variables and validate it
def GetPluginParams():
	env_vars = os.environ

	WebHookURL = str(env_vars.get("NOTIFY_PARAMETER_1"))

	# "None", if not in the environment variables
	if (WebHookURL == "None"):
		print("ifttt-plugin: Mandatory first parameter is missing: Webhook URL")
		return 2, "" 	# do not return anything, create final error
	
	if "https://hooks.zapier.com/hooks/catch" not in WebHookURL:  #### TBD
		print(f"ifttt-plugin: Parameter 1 is not a URL starting with https://hooks.zapier.com/hooks/catch: {WebHookURL}")
		return 2, ""	# do not return anything, create final error

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
def StartStartIftttWorkflow(WebHookURL, data):
	return_code = 0

    # Set header information
	headers = {
        'Content-Type': 'application/json'
    }

	try:
        # Make the POST request to start the workflow
		response = requests.post(WebHookURL, headers=headers, json=data)

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

	return_code = StartStartIftttWorkflow(WebHookURL, data)

	return return_code


if __name__ == '__main__':
	sys.exit(main())

