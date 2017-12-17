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

sc.rtm_connect()
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
                    unit = artcbot.get_unit(message[3])
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
                unit = artcbot.get_unit(message[2])
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
                    unit = artcbot.get_unit(message[2])
                message = artcbot.convert(1,distance,unit,1,command)
                sendMessage(user, channel, message) 
            elif events["text"].startswith(("!planner")):
                channel = getChannel(events)
                user = getUser(events)
                message = events["text"].split(' ')
                command = message[0]
                message = artcbot.planner(message[1],message[2])
                sendMessage(user, channel, message)
            elif events["text"].startswith(("I'm")):
                channel = getChannel(events)
                user = getUser(events)
                message = events["text"].split(' ')
                if(len(message) < 6 and random.randint(0,3) > 2):
                    del message[0]
                    message = " ".join(message)
                    response = "Hi "+message+" I'm artcbot."
                    sendMessage(user, channel, response)
            elif events["text"].startswith(("!trainingpaces")):
                channel = getChannel(events)
                user = getUser(events)
                message = events["text"].split(' ')
                #cheating and copying the vdot command
                #NOT WORKING FOR JD
                command = message[0]
                if(len(message) > 2):
                    raceTime = message[1].split(':')
                    if(len(raceTime) < 3):
                        raceTime = float(raceTime[0])+float(raceTime[1])/60.0
                    elif(len(raceTime) == 3):
                        raceTime = float(raceTime[0])*60.0+float(raceTime[1])+float(raceTime[2])/60.0
                    if (len(message) == 3):
                        (distance, unit) = parseDistance(message[2])
                    else:
                        distance = float(message[2])
                        unit = artcbot.get_unit(message[3])
                    message = artcbot.convert(raceTime,distance,unit,message[1],command)
                else:
                    message = float(message[1])
                message = "```"+artcbot.trainingpaces(round(message,0))+"```"
                sendMessage(user, channel, message) 
            #Has to be last elif
            elif events["text"].startswith("!"):
                channel = getChannel(events)
                user = getUser(events)
                message = events["text"].split(' ')
                command = message[0]
                index = command_list.index(command)
                message = codecs.decode(command_list[index+1], 'unicode_escape')
                sendMessage(user, channel, message)
    
    time.sleep(1)
