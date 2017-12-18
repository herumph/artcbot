import artcbot
import os
import re
import time
import codecs
import random
from slackclient import SlackClient

slack_token = os.environ["SLACK_BOT_TOKEN"]
sc = SlackClient(slack_token)

#getting arrays
command_list = artcbot.get_array("command_list")
built_in = ["add","edit","delete","vdot","planner","pacing","splits","convertpace","convertdistance","trainingpaces"]
#I'm lazy
built_in = ["!"+i for i in built_in]

def sendMessage(user, channel, message):
    sc.api_call(
        "chat.postMessage",
        username = "artcbot",
        icon_emoji = ":robot_face:",
        channel=channel,
        link_names=1,
        text= '<@'+user +'>' +' '+ message)      

def getChannel(event):
    return event['channel']

def getUser(event):
    return event['user']

#getting slack text events and responding
sc.rtm_connect()
while True:
    new_events = sc.rtm_read()
    for events in new_events:
        if(events["type"] == "message"):
            message = events["text"].split(' ')
            command = list(set(message).intersection(command_list))
            function = list(set(message).intersection(built_in))
            if(len(command) > 0 or len(function) > 0):
                channel = getChannel(events)
                user = getUser(events)
                #sending contributors as an empty list, no editing of commands on slack
                message = artcbot.call_bot(message, user, [])
                if(len(message) > 1): sendMessage(user, channel, message)
    time.sleep(1)

###########################
#not used (possibly broken)
def parseDistance(orig):
    dist = 0
    unit = 'na'

    if (type(orig) == str):
        ary = orig.split()
    else:
        ary = orig

    if (len(ary) == 1):
        m = re.match(r'([0-9.]+)([A-Za-z]+)', ary[0])
        if m:
            dist = float(m.group(1))
            unit = m.group(2)
    elif (len(ary) == 2):
        dist = float(ary[0])
        unit = ary[1]

    if (unit.startswith(('km', 'ki')) or unit == 'k'):
        unit = 'kilometer(s)'
    elif (unit.startswith('mi') or unit == 'm'):
        unit = 'mile(s)'

    return [dist, unit]