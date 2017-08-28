import artcbot
import os
import re
import time
from slackclient import SlackClient

slack_token = os.environ["SLACK_BOT_TOKEN"]
sc = SlackClient(slack_token)


def sendMessage(user, channel, message):
    sc.api_call(
        "chat.postMessage",
        username = "Patriots Bot",
        icon_emoji = ":elvis:",
        channel=channel,
        link_names=1,
        text= '<@'+user +'>' +' '+ message)      

def getChannel(event):
    return event['channel']

def getUser(event):
    return event['user']

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
        unit = 'kilometer'
    elif (unit.startswith('mi')):
        unit = 'mile'

    return [dist, unit]


if sc.rtm_connect():
    while True:
        new_events = sc.rtm_read()
        for events in new_events:
            if events["type"] == "message":
                #convert pace
                if events["text"].startswith(("!pacing","!vdot")):
                    channel = getChannel(events)
                    user = getUser(events)
                    message = events["text"].split(' ')
                    command = message[0]
                    raceTime = message[1].split(':')
                    if(len(raceTime) < 3):
                        raceTime = float(raceTime[0])+float(raceTime[1])/60.0
                    elif(len(raceTime) == 3):
                        raceTime = float(raceTime[0])*60.0+float(raceTime[1])+float(raceTime[2])/60.0
                    if (len(message) == 3):
                        (distance, unit) = parseDistance(message[2])
                    else:
                        distance = float(message[2])
                        unit = message[3]
                    message = artcbot.convert(raceTime,distance,unit,message[1],command)
                    sendMessage(user, channel, message) 
                elif events["text"].startswith(("!convertpace","!splits")):
                    channel = getChannel(events)
                    user = getUser(events)
                    message = events["text"].split(' ')
                    command = message[0]
                    raceTime = message[1].split(':')
                    if(len(raceTime) < 3):
                        raceTime = float(raceTime[0])+float(raceTime[1])/60.0
                    elif(len(raceTime) == 3):
                        raceTime = float(raceTime[0])*60.0+float(raceTime[1])+float(raceTime[2])/60.0
                    unit = message[2]
                    message = artcbot.convert(raceTime,1,unit,message[1],command)
                    sendMessage(user, channel, message) 
                elif events["text"].startswith(("!convertdistance")):
                    channel = getChannel(events)
                    user = getUser(events)
                    message = events["text"].split(' ')
                    command = message[0]
                    if (len(message) == 2):
                        (distance, unit) = parseDistance(message[1])
                    else:
                        distance = float(message[1])
                        unit = message[2]
                    message = artcbot.convert(1,distance,unit,1,command)
                    sendMessage(user, channel, message) 
        time.sleep(1)
else:
    print "Connection Failed, invalid token?"

