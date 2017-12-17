#ARTCbot. Responds to ! commands 
#To do list:
#1 - Calendar integration? !upcoming <user> and !upcoming
#2 - PM integration for everything
#3 - Paces from other places. BT, etc. 

import codecs
from datetime import datetime, timedelta
from math import exp

#Functions to read and write files into arrays.
def get_array(input_string):
    with open("textfiles/"+input_string+".txt","r") as f:
        input_array = f.readlines()
    input_array = [x.strip("\n") for x in input_array]
    return(input_array)

def write_out(input_string,input_array):
    with open("textfiles/"+input_string+".txt","w") as f:
        for i in input_array:
            f.write(i+"\n")
    return

#Fetching arrays
command_list = get_array("command_list")
jd_paces = get_array("jd_paces")
pf_paces = get_array("pf_paces")
han_paces = get_array("han_paces")
#Defining built in commands
built_in = ["add","edit","delete","vdot","planner","pacing","splits","convertpace","convertdistance","trainingpaces"]

#getting pace information, first element are the labels
jd_paces = [i.split(',') for i in jd_paces]
pf_paces = [i.split(',') for i in pf_paces]
han_paces = [i.split(',') for i in han_paces]

#Defining VDOT ranges.
vdot_range=[30.0,85.0]

#Return date to start training
def planner(date,time):
    formatting = date.split('/')
    #Checking the date format
    if(len(formatting[0]) > 2 or len(formatting[1]) > 2 or len(formatting[2]) > 2):
        return "Your date is the wrong format. Please put your date in mm/dd/yy format."
    date = datetime.strptime(date, "%m/%d/%y")
    time_new = date - timedelta(weeks=int(time))
    return "For a "+time+" week plan, start training on "+str(time_new.month)+"/"+str(time_new.day)+"/"+str(time_new.year)+"."

#Get the time from a comment and return seconds
def get_time(time):
    time = time.split(':')
    if(len(time) < 3):
        return float(time[0])+float(time[1])/60.0
    elif(len(time) == 3):
        return float(time[0])*60.0+float(time[1])+float(time[2])/60.0

#Time formatting function. Time given in minutes as a float.
def time_format(time):
    minutes = int(time % 100)
    seconds = int((time % 1)*60)
    str_seconds = str(seconds)
    if(seconds < 10):
        str_seconds = "0"+str(seconds)
    return (minutes, str_seconds)
    
#Calculating VDOT
#Time given in minutes as a float, distance as a float in kilometers
def VDOT(time, distance):
    num = -4.6+0.182258*(distance*1e3/time)+0.000104*(distance*1e3/time)**2
    denom = 0.8+0.1894393*exp(-0.012778*time)+0.2989558*exp(-0.1932605*time)
    return round(num/denom,1)

#Conversion function
#Time in minutes as a float, distance as a float, unit as a string, inputs as a string, string is obvious.
def convert(time, distance, unit,inputs, string):
    if(unit == "mile(s)"):
        distance_conversion = str(round(distance*1.60934,1))
        time_conversion = time/1.60934
        minutes, str_seconds = time_format(time_conversion)
        time_sec = time*60.0
        split = int(400.0*time_sec/1609.0)
        split_perm = time_sec/(float(distance)*60.0)
        minutes_perm, str_seconds_perm = time_format(split_perm)
        split_perk = time_sec/(float(distance_conversion)*60.0)
        minutes_perk, str_seconds_perk = time_format(split_perk)
        v_dot = VDOT(time,float(distance_conversion))

        #Checking command
        if(string == "!convertdistance"):
            message = str(distance)+" miles is "+distance_conversion+" kilometers."
        if(string == "!convertpace"):
            message = "A "+inputs+" mile is a "+str(minutes)+":"+str_seconds+" kilometer."
        if(string == "!splits"):
            message = "For a "+inputs+" mile, run "+str(split)+" second 400s."
        if(string == "!pacing"):
            message = "To run "+str(distance)+" "+unit+" in "+inputs+" you need to run each mile in "+str(minutes_perm)+":"+str_seconds_perm+", or each kilometer in "+str(minutes_perk)+":"+str_seconds_perk+"."

    if(unit == "kilometer(s)"):
        distance_conversion = str(round(distance/1.60934,1))
        time_conversion = time*1.60934
        minutes, str_seconds = time_format(time_conversion)
        time_sec = time*60.0
        split = int(400.0*time_sec/1000.0)
        split_perk = time_sec/(float(distance)*60.0)
        minutes_perk, str_seconds_perk = time_format(split_perk)
        split_perm = time_sec/(float(distance_conversion)*60.0)
        minutes_perm, str_seconds_perm = time_format(split_perm)
        v_dot = VDOT(time,distance)

        #Checking command
        if(string == "!convertdistance"):
            message = str(distance)+" kilometers is "+distance_conversion+" miles."
        if(string == "!convertpace"):
            message = "A "+inputs+" kilometer is a "+str(minutes)+":"+str_seconds+" mile."
        if(string == "!splits"):
            message = "For a "+inputs+" kilometer, run "+str(split)+" second 400s."
        if(string == "!pacing"):
            message = "To run "+str(distance)+" "+unit+" in "+inputs+" you need to run each kilometer in "+str(minutes_perk)+":"+str_seconds_perk+", or each mile in "+str(minutes_perm)+":"+str_seconds_perm+"."
    
    if(string == "!vdot" or string == "!trainingpaces"):
        message = "A "+inputs+" "+str(distance)+" "+unit+" corresponds to a "+str(v_dot)+" VDOT."
    if(string == "!trainingpaces"):
        message = "A "+inputs+" "+str(distance)+" "+unit+" corresponds to a "+str(v_dot)+" VDOT."
        return [message,v_dot]


    return message 

#Add/Edit/Delete user commands function
#split into small functions
def aed(comment_list,comment,author):
    #Adding commands
    if(comment_list.count("!add")):
        index = comment_list.index("!add")
        add_command = comment_list[index+1]

        #Searching if command already exists.
        if("!"+add_command in command_list):
            reply = ("The command !"+add_command+" already exists. Please try !edit instead.")
            return reply

        #Stopping people from overwriting built in commands
        if(add_command in built_in):
            reply = ("That command cannot be added as it's built into my programming. Please try a different name.")
            return reply

        #Taking the rest of the comment as the new command and stripping it downs
        new_command = comment.replace("!add","")
        new_command = new_command.replace(add_command,"",1)
        new_command = new_command.lstrip()
    
        #Stopping command responses that start with !
        if(add_command[0] == "!" or new_command[0] == "!"):
            reply = "That command cannot be added because it either has an extra ! in the command or the response starts with !\n\n The command is `!add new_command response."
            return reply

        #Human friendly version of the edit
        temp = new_command
        new_command = new_command.splitlines()
        #Doing fancy shit to make the commands work
        new_command = r'\n'.join(map(str, new_command))
        #Actually adding the command
        command_list.append("!"+add_command)
        command_list.append(new_command)
        write_out('command_list',command_list) 
        reply = "Successfully added !"+add_command+"\n\n The new response is:\n\n"+temp
        return reply

    #Deleting commands
    elif(comment_list.count("!delete")):
        index = comment_list.index("!delete")
        delete_command = comment_list[index+1]
        command_index = command_list.index("!"+delete_command)
        #Actually deleting command
        del command_list[command_index]
        del command_list[command_index]
        write_out('command_list',command_list)
        reply = "Successfully deleted !"+delete_command
        return reply

    elif(comment_list.count("!edit")):
        #Editing commands
        index = comment_list.index("!edit")
        edit_command = comment_list[index+1]
        #Taking the rest of the comment as the new command and stripping it down
        new_command = comment.replace("!edit","")
        new_command = new_command.replace(edit_command,"",1)
        new_command = new_command.lstrip()
        #Human friendly version of the edit
        temp = new_command
        new_command = new_command.splitlines()
        #Doing fancy shit to make the commands work
        new_command = r'\n'.join(map(str, new_command))
        #Making sure the command exists
        if("!"+edit_command not in command_list):
            reply = "That command does not exist. Try !add instead."
            return reply
            
        #Actually replacing the command
        command_index = command_list.index("!"+edit_command)
        #Easier to delete both old command and response and append the new ones
        del command_list[command_index] 
        del command_list[command_index]
        command_list.append("!"+edit_command)
        command_list.append(new_command)
        write_out('command_list',command_list)
        reply = "Successfully edited !"+edit_command+"\n\n The new response is:\n\n"+temp
        return reply

#Responding to help commands
def help(comment_list):
    #Having to convert back from raw string
    index = command_list.index("!help")
    reply = codecs.decode(command_list[index+1], 'unicode_escape')
    reply += "\n\n **Community made commands and quick links are:** \n\n"
    for i in range(0,len(command_list)-1,2):
        if(i != index and i < len(command_list)-2):
            reply += command_list[i]+", "
    reply += "\n\n**I can reply to multiple commands at a time, so don't be picky.**"
    return reply

#Paces based on VDOT
def trainingpaces(v_dot):
    reply = ""
    #input array, input string for labels 
    reply1 = pace_table(jd_paces[1:], jd_paces[0], v_dot, "Jack Daniels")
    #checking to make sure the no listed paces output isn't the response
    if(not reply1.count("There")):
        reply += "\n\n For a "+str(v_dot)+" VDOT here are training paces from popular books."
        reply += reply1
        reply += pace_table(pf_paces[1:], pf_paces[0], v_dot, "Pfitz")
        reply += pace_table(han_paces[1:], han_paces[0], v_dot, "Hansons")
    else:
        reply += reply1
    return reply

#Returning a reddit formatted table for an input vdot
def pace_table(input_array, input_string, v_dot, source):
    reply = ""
    for i in range(0,len(input_array)-1,1):
        #it was being weird so now I have weird conditionals to make it work
        if(float(input_array[i][0]) == v_dot):
            reply = make_table(input_array, input_string, source, i)
            break;
        elif(float(input_array[i+1][0]) == v_dot):
            reply = make_table(input_array, input_string, source, i+1)
            break;
        elif(float(input_array[i][0]) <= v_dot and float(input_array[i+1][0]) >= v_dot):
            reply = make_table(input_array, input_string, source, i)
            break;
    if(float(v_dot) < min(vdot_range) or float(v_dot) > max(vdot_range)):
        reply = "\n\nThere are no listed training paces for a "+str(v_dot)+" VDOT."
    return reply

def make_table(input_array, input_string, source, index):
    reply = "\n\n **"+source+"**\n\n"
    for j in range(1,len(input_string)):
        reply += input_string[j]+' | '
    table_break = " -- |"*len(input_string)
    reply += "\n"+table_break+"\n"
    for j in range(1,len(input_array[index])):
        reply += input_array[index][j]+" | "
    return reply

#stealing what tapin did for the slack version
def get_unit(unit):
    if (unit.startswith(('km', 'ki')) or unit == 'k'):
        return 'kilometer(s)'
    elif (unit.startswith('mi') or unit == 'm'):
        return 'mile(s)'
    return
