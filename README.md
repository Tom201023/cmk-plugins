# cmk-plugins
Various plugins for Checkmk

This is the GitHub plase for all the Checkmk plugins I will develop, starting with the ntfy plugin

# ntfy-plugin
Sends notifications to mobile phones (iOS and Android) using the ntfy.sh service 
For details please check https://ntfy.sh
Install the ntfy app on iOS and Android on your phone
 
Checkmk usage
Select the 'ntfy-plugin' as notification plugin
Paramater 1 (mandatory): Provide a unique topic, which you also need to add in the app
Parameter 2 (optional): Provide an access token in the format 'Bearer tk_AgQdq7mVBoFD37zQVN29RhuMzNIz2'

Some additional noteworthy comments
 - In FREE mode, you can send only 250 messages per day. Sufficient for home usage or testing, but get an account if you are a company.
 - To reserve a topic exclusively for your, you need an account. For testing or home usage, just select a topic, which us unique
 - For testing, the plugin can be used without an access token
 - Error messages are written to ~/var/log/notify.log. In case of any issue, please have a look there
 - This is my first Python program. Please look at it with clemency. I used VC Code with Pydantic (type checking mode: Basic) and Black
