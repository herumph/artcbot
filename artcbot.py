#!/Users/sfdavis/anaconda3/bin/python

#ARTCbot. Responds to ! commands 
#Updating the !help is going to be the most difficult to keep up with 

import praw
from config_bot import *
import codecs

#Reddit stuff
r = praw.Reddit("ARTCbot 1.0 by herumph")
r.login(REDDIT_USERNAME, REDDIT_PASS)
#subreddit = r.get_subreddit("RumphyBot")
subreddit = r.get_subreddit("artc")
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

print("\n * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * \n")

#Getting subreddit contributors
contributors=[]
for contributor in subreddit.get_contributors():
	contributors.append(str(contributor))
#print(contributors)

#Sorting through comments and replying
#print(command_list)
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
		if("!"+add_command in command_list):
			comment.reply("The command !"+add_command+" already exists. Please try !edit instead.")
			break
		#Taking the rest of the comment as the new command and stripping it downs
		#new_command = comment_list[index+2:]
		#print(new_command)
		new_command = str(comment.body).replace("!add","")
		new_command = new_command.replace(add_command,"",1)
		new_command = new_command.lstrip()
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
		if("!"+new_command not in command_list):
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
		
	#Replying to users not allower to edit comments
	if(comment.body.count("!edit") and comment.id not in already_done and str(comment.author) not in contributors and str(comment.author) != "artcbot"):
		already_done.append(comment.id)
		write_out("already_done",already_done)
		comment.reply("Sorry, you are not allowed to edit commands.")
		
	if(comment.body.count("!add") and comment.id not in already_done and str(comment.author) not in contributors and str(comment.author) != "artcbot"):
		already_done.append(comment.id)
		write_out("already_done",already_done)
		comment.reply("Sorry, you are not allowed to edit commands.")
		
	if(comment.body.count("!delete") and comment.id not in already_done and str(comment.author) not in contributors and str(comment.author) != "artcbot"):
		already_done.append(comment.id)
		write_out("already_done",already_done)
		comment.reply("Sorry, you are not allowed to edit commands.")
	
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