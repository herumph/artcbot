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
                    distance = float(message[1])
                    unit = message[2]
                    message = artcbot.convert(1,distance,unit,1,command)
                    sendMessage(user, channel, message) 
        time.sleep(1)
else:
    print "Connection Failed, invalid token?"

