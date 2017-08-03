#!/Users/sfdavis/anaconda3/bin/python

#ARTCbot. Responds to ! commands 
#Updating the !help is going to be the most difficult to keep up with 

import praw
from config_bot import *
import codecs
from datetime import datetime, timedelta
from math import exp

#Reddit stuff
r = praw.Reddit("ARTCbot 1.1 by herumph")
r.login(REDDIT_USERNAME, REDDIT_PASS)
subreddit = r.get_subreddit("RumphyBot")
#subreddit = r.get_subreddit("artc")
subreddit_comments = subreddit.get_comments()

#Functions to read and write files into arrays.
def get_array(input_string):
    with open(input_string+".txt","r") as f:
        input_array = f.readlines()
    input_array = [x.strip("\n") for x in input_array]
    return(input_array)

def write_out(input_string,input_array):
    with open(input_string+".txt","w") as f:
        for i in input_array:
            f.write(i+"\n")
    return

#Fetching arrays
already_done = get_array("already_done")
command_list = get_array("command_list")
#Defining built in commands
built_in = ["add","edit","delete","vdot","planner","pacing","splits","convertpace","convertdistance"]

print("\n * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * \n")

#Getting subreddit contributors
contributors=[]
for contributor in subreddit.get_contributors():
    contributors.append(str(contributor))

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
    if(unit == "miles" or unit == "m" or unit == "mile"):
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

    if(unit == "kilometers" or unit == "km" or unit == "kilometer"):
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
            message = str(distance)+" kilometers is "+distance_conversion+" ~~freedom units~~ miles."
        if(string == "!convertpace"):
            message = "A "+inputs+" kilometer is a "+str(minutes)+":"+str_seconds+" mile."
        if(string == "!splits"):
            message = "For a "+inputs+" kilometer, run "+str(split)+" second 400s."
        if(string == "!pacing"):
            message = "To run "+str(distance)+" "+unit+" in "+inputs+" you need to run each kilometer in "+str(minutes_perk)+":"+str_seconds_perk+", or each mile in "+str(minutes_perm)+":"+str_seconds_perm+"."
    
    if(string == "!vdot"):
        message = "A "+inputs+" "+str(distance)+" "+unit+" corresponds to a "+str(v_dot)+" VDOT."

    #Replying
    comment.reply(message)
    return

#Sorting through comments and replying
for comment in subreddit_comments:
	#Adding commands
    if(comment.body.count("!add") and comment.id not in already_done and str(comment.author) in contributors and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        comment_list = str(comment.body)
        comment_list = comment_list.split()
        #Finding command to add
        index = comment_list.index("!add")
        add_command = comment_list[index+1]
        #Searching if command already exists.
        if("!"+add_command in command_list):
            comment.reply("The command !"+add_command+" already exists. Please try !edit instead.")
            break
        #Stopping people from overwriting built in commands
        if(add_command in built_in):
            comment.reply("That command cannot be added as it's built into my programming. Please try a different name.")
            break
        #Taking the rest of the comment as the new command and stripping it downs
        new_command = str(comment.body).replace("!add","")
        new_command = new_command.replace(add_command,"",1)
        new_command = new_command.lstrip()
        #Stopping command responses that start with !
        if(add_command[0] == "!" or new_command[0] == "!"):
            comment.reply("That command cannot be added because it either has an extra ! in the command or the response starts with !\n\n The command is `!add new_command response`")
            break
        #Human friendly version of the edit
        temp = new_command
        new_command = new_command.splitlines()
        #Doing fancy shit to make the commands work
        new_command = r'\n'.join(map(str, new_command))
        #Actually adding the command
        command_list.append("!"+add_command)
        command_list.append(new_command)
        write_out('command_list',command_list)
        comment.reply("Successfully added !"+add_command+"\n\n The new response is:\n\n"+temp)

    #Deleting commands
    if(comment.body.count("!delete") and comment.id not in already_done and str(comment.author) in contributors and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        comment_list = str(comment.body)
        comment_list = comment_list.split()
        #Finding command user wants to delete
        index = comment_list.index("!delete")
        delete_command = comment_list[index+1]
        command_index = command_list.index("!"+delete_command)
        #Actually deleting command
        del command_list[command_index]
        del command_list[command_index]
        write_out('command_list',command_list)
        comment.reply("Successfully deleted !"+delete_command)

    #Editing commands
    if(comment.body.count("!edit") and comment.id not in already_done and str(comment.author) in contributors and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        comment_list = str(comment.body)
        comment_list = comment_list.split()
        #Finding command user wants to edit
        index = comment_list.index("!edit")
        edit_command = comment_list[index+1]
        #Taking the rest of the comment as the new command and stripping it down
        new_command = str(comment.body).replace("!edit","")
        new_command = new_command.replace(edit_command,"",1)
        new_command = new_command.lstrip()
        #Human friendly version of the edit
        temp = new_command
        new_command = new_command.splitlines()
        #Doing fancy shit to make the commands work
        new_command = r'\n'.join(map(str, new_command))
        #Making sure the command exists
        if("!"+edit_command not in command_list):
            comment.reply("That command does not exist. Try !add instead.")
            break
        #Actually replacing the command
        command_index = command_list.index("!"+edit_command)
        #Easier to delete both old command and response and append the new ones
        del command_list[command_index]
        del command_list[command_index]
        command_list.append("!"+edit_command)
        command_list.append(new_command)
        write_out('command_list',command_list)
        comment.reply("Successfully edited !"+edit_command+"\n\n The new response is:\n\n"+temp)

    #Replying to users not allowed to edit comments
    if(comment.body.count("!edit") and comment.id not in already_done and str(comment.author) not in contributors and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        comment.reply("Sorry, you are not allowed to edit commands.")
	
    #Replying to users not allowed to add commands
    if(comment.body.count("!add") and comment.id not in already_done and str(comment.author) not in contributors and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        comment.reply("Sorry, you are not allowed to edit commands.")

	#Replying to users not allowed to delete commands
    if(comment.body.count("!delete") and comment.id not in already_done and str(comment.author) not in contributors and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        comment.reply("Sorry, you are not allowed to edit commands.")
        
    #Help command
    if(comment.body.count("!help") and comment.id not in already_done and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        index = command_list.index("!help")
        #Having to convert back from raw string
        reply = codecs.decode(command_list[index+1], 'unicode_escape')
        reply += "\n\n **Community made commands and quick links are:** \n\n"
        for i in range(0,len(command_list)-1,2):
            if(i != index and i < len(command_list)-2):
                reply += command_list[i]+", "
            elif(i != index):
                reply += command_list[i]
        comment.reply(reply)

    #Splitting up the comment text by white space and seeing if it has any commands
    comment_list = str(comment.body)
    comment_list = comment_list.split()
    common = list(set(comment_list).intersection(command_list))
    #Replying if there is a command
    if(len(common) > 0 and comment.id not in already_done and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        command_index = command_list.index(common[0])
        #Having to convert back from raw string
        reply = codecs.decode(command_list[command_index+1], 'unicode_escape')
        comment.reply(reply)

    #Converting distances between km and miles, and vise versa.
    if(comment.body.count("!convertdistance") and comment.id not in already_done and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        index = comment_list.index("!convertdistance")
        unit = comment_list[index+2].lower()
        distance = comment_list[index+1]
        distance = float(distance)
        convert(1, distance, unit, 1,"!convertdistance")

    #Converting paces between km/min and miles/min, and vise versa
    if(comment.body.count("!convertpace") and comment.id not in already_done and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        index = comment_list.index("!convertpace")
        unit = comment_list[index+2].lower()
        time = comment_list[index+1]
        time = time.split(':')
        if(len(time) < 3):
            time = float(time[0])+float(time[1])/60.0
        elif(len(time) == 3):
            time = float(time[0])*60.0+float(time[1])+float(time[2])/60.0
        convert(time, 1, unit, comment_list[index+1], "!convertpace")

    #Track split calculator
    if(comment.body.count("!splits") and comment.id not in already_done and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        index = comment_list.index("!splits")
        unit = comment_list[index+2].lower()
        time = comment_list[index+1]
        time = time.split(':')
        if(len(time) < 3):
            time = float(time[0])+float(time[1])/60.0
        elif(len(time) == 3):
            time = float(time[0])*60.0+float(time[1])+float(time[2])/60.0
        convert(time, 1, unit, comment_list[index+1], "!splits")

    #Training plan calculator
    if(comment.body.count("!planner") and comment.id not in already_done and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        index = comment_list.index("!planner")
        date = comment_list[index+1]
        formatting = date.split('/')
        #Checking the date format
        if(len(formatting[0]) > 2 or len(formatting[1]) > 2 or len(formatting[2]) > 2):
            comment.reply("Your date is the wrong format. Please put your date in mm/dd/yy format.")
            break
        time= comment_list[index+2]
        date = datetime.strptime(date, "%m/%d/%y")
        time_new = date - timedelta(weeks=int(time))
        comment.reply("For a "+time+" week plan, start training on "+str(time_new.month)+"/"+str(time_new.day)+"/"+str(time_new.year)+".")

    #Race pace calculator
    if(comment.body.count("!pacing") and comment.id not in already_done and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        index = comment_list.index("!pacing")
        time = comment_list[index+1]
        time = time.split(':')
        distance = float(comment_list[index+2])
        unit = comment_list[index+3].lower()
        if(len(time) < 3):
            time = float(time[0])+float(time[1])/60.0
        elif(len(time) == 3):
            time = float(time[0])*60.0+float(time[1])+float(time[2])/60.0
        convert(time, distance, unit, comment_list[index+1], "!pacing")
        
    #VDOT calculator
    if(comment.body.count("!vdot") and comment.id not in already_done and str(comment.author) != "artcbot"):
        already_done.append(comment.id)
        write_out("already_done",already_done)
        index = comment_list.index("!vdot")
        time = comment_list[index+1]
        time = time.split(':')
        distance = float(comment_list[index+2])
        unit = comment_list[index+3].lower()
        if(len(time) < 3):
            time = float(time[0])+float(time[1])/60.0
        elif(len(time) == 3):
            time = float(time[0])*60.0+float(time[1])+float(time[2])/60.0
        convert(time, distance, unit, comment_list[index+1], "!vdot")