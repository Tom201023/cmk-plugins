# cmk-plugins
Various plugins for Checkmk

This is the GitHub plase for all the Checkmk plugins I have developed and published on the Checkmk Exchange

# ntfy-plugin
Sends notifications to mobile phones (iOS and Android) using the ntfy.sh service 
For details please check https://ntfy.sh
Install the ntfy app on iOS and Android on your phone
 
### Checkmk usage
Select the 'ntfy-plugin' as notification plugin
- Parameter 1 (mandatory): Provide a unique topic, which you also need to add in the app
- Parameter 2 (optional): Provide an access token in the format 'Bearer tk_AgQdq7mVBoFD37zQVN29RhuMzNIz2'

### Some additional comments
 - In FREE mode, you can send only 250 messages per day. Sufficient for home usage or testing, but get an account if you are a company.
 - To reserve a topic exclusively for your, you need an account. For testing or home usage, just select a topic, which us unique
 - For testing, the plugin can be used without an access token
 - Error messages are written to ~/var/log/notify.log. In case of any issue, please have a look there
 - This is my first Python program. Please look at it with clemency. I used VC Code with Pydantic (type checking mode: Basic) and Black

# Tines-plugin
Sends notifications to tines.com for infrastructure and security automation
For details, please check https://www.tines.com

### Checkmk usage
Select the 'tines-plugin' as notification plugin
- Mandatory parameter Tines Webhook URL: Provide the Webhook URL copied from a Webhook task in Tines, which is the starting point for your workflow

### Some additional comments
- In the community (free) mode, you can only start 500 workflows (also called stories) per day, and you are limited to 3 different stories
- Error messages are written to ~/var/log/notify.log. In case of any issue, please have a look there
- implemented using VC Code with Pydantic (type checking mode: Basic) and Black

# Zapier-plugin
Sends notifications to Zapier.com for all types of automation
For details, please check https://www.zapier.com
  
### Checkmk usage
Select the 'zapier-plugin' as the notification plugin
- Parameter 1 (mandatory): Provide the webhook URL copied from a webhook task in Zapier that is the starting point for your workflow
 
### Some additional comments
- Unfortunately, Zapier requires a paid subscription to use a webhook task.
- You can get a free trial for the first 14 days.
- Zapier limitations: 10,000 webhook calls/5 minutes and 30 webhook calls/30 seconds (https://help.zapier.com/hc/en-us/articles/8496288690317#h_01HBGES5DWAJT066TDGX3G6R0G) 
- No retry after receiving a 429 error for exceeding these limits
- Error messages are written to ~/var/log/notify.log. Please take a look there if you encounter any problems.
- implemented with VC Code using Pydantic (type checking mode: Basic) and Black

# ifttt-plugin
Sends notifications to IFTTT.com (If This, Then That) for all types of automation
See https://www.ifttt.com for details
  
### Checkmk usage
Select the 'ifttt-plugin' as the notification plugin
- Parameter 1 (mandatory): The event name defined for the webhook, e.g. 'cmk_notification'
- Parameter 2 (mandatory): Your personal IFTTT account key, e.g. '0_1ft9AyL1zB2Lx3sC456'

### Some additional comments
- You can find your IFTTT key here: My Services > Webhooks > Settings
- Error messages will be written to ~/var/log/notify.log. Please take a look there if you encounter any problems.
- implemented with VC Code using Pydantic (type checking mode: Basic) and Black
