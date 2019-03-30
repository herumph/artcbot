import artcbot
import os
import re
import time
import codecs
import random
from slackclient import SlackClient
from datetime import datetime
import requests

slack_token = os.environ["SLACK_BOT_TOKEN"]
sc = SlackClient(slack_token)

# welcome message
welcomeMessage = "Welcome to slack, you are automatically added to the channels #random and #general." + \
    " If you click 'channels' on the left side of your screen, you can also look through other channels you can join." + \
    "\n\nYou can also directly message users with the option below your channels." + \
    " In a chat, you can specifically get the attention of a user by writing @theirusername, similar to Twitter." + \
    "\n\nTo use emojis type `:emojiname:` or click the add emoji option in your message box." + \
    " You can also react to people's messages with emoji by clicking their message and " + \
    "the add reaction button, then selecting the emoji you feel is appropriate." + \
    "\n\nAlso, if you have a concern about your full name being displayed." + \
    " You can go to the dropdown in the top left of your page, and go to 'profile and account' and then click 'edit profile.'" + \
    " From there, you can change how your full name appears in the profile other users can see."

# getting arrays
command_list = artcbot.get_array("command_list")
built_in = artcbot.get_array("built_in")
built_in = ["!"+i for i in built_in]

def errorMessage(user):
    errors = ["Something went wrong :party_rip:",
                "Oh no you killed artcbot",
                "Your command is bad and you should feel bad",
                "artcbot is taking a vacation :palm_tree:",
                "Here lies artcbot. Viciously murdered by <@"+user+"> :rip:"]
    return errors[random.randint(0, len(errors)-1)]


def sendMessage(user, channel, message):
    sc.api_call(
        "chat.postMessage",
        username = "artcbot",
        icon_emoji = ":blob_elf:",
        channel=channel,
        link_names=1,

        text= '<@'+user +'>' +' '+ message)

def getChannel(event):
    return event['channel']

def getUser(event):
    return event['user']

# getting slack text events and responding
sc.rtm_connect()
#sc.api_call("channel_list", token = slack_token)

#users = sc.api_call("users.list", token = slack_token)
#old_names = [x['id'] for x in users['members']]
#artcbot.write_out("names",old_names)
#print('written')

then = datetime.now()
while True:
    now = datetime.now()

    # welcome message, checking every minute
    if(now.minute != then.minute):
        then = now
        users = sc.api_call("users.list", token = slack_token)
        new_names = [x['id'] for x in users['members']]
        old_names = artcbot.get_array("names")
        if(new_names != old_names):
            s = set(old_names)
            newUsers = [x for x in new_names if x not in s]
            # PMing
            for x in newUsers:
                sendMessage(x, x, welcomeMessage)
            old_names = new_names
            artcbot.write_out("names",old_names)

    new_events = sc.rtm_read()
    for events in new_events:
        if(events["type"] == "message" or events["type"] == "file_created"):
            channel = getChannel(events)

            # it is wednesday, my dudes
            if(channel == "C78G97C9F" and now.weekday() == 2): # dumbmemes
            #if(channel == "C50T5QMQ8"): #BARTC
                user = getUser(events)
                sc.api_call("reactions.add", token = slack_token, name = 'wednesday', channel = channel, timestamp = events['ts'])

            # adding a try here so the bot hopefully stops crashing all the time when it can't split a message
            try:
                message = events["text"].split(' ')
            except:
                pass

            command = list(set(message).intersection(command_list))
            function = list(set(message).intersection(built_in))
            if(len(command) > 0 or len(function) > 0):
                user = getUser(events)
                # sending user id(s) as contributor(s)
                try:
                    message = artcbot.call_bot(message, user, ['U4Z02CNN6'])
                    if(len(message) > 1): sendMessage(user, channel, message)
                except:
                    sendMessage(user, channel, errorMessage(user))

            if("<@U6L8TPTCZ>" in message): # responding to tags
                user = getUser(events)
                message = "no u"
                sendMessage(user, channel, message)
    time.sleep(1)
