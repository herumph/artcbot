import artcbot
import praw
from config_bot import *

#Reddit stuff
r = praw.Reddit(user_agent = "ARTCbot 1.3.0 by herumph",
        client_id = ID,
        client_secret = SECRET,
        username = REDDIT_USERNAME,
        password = REDDIT_PASS)

#sub = "artc"
sub = "RumphyBot"
subreddit = r.subreddit(sub)

#Fetching arrays
already_done = artcbot.get_array("already_done")
#not ideal to get contributors every time but it's not a problem
contributors = [str(contributor) for contributor in r.subreddit(sub).contributor()]

#Looking at comments
for comment in r.subreddit(sub).comments(limit=25):
    reply = ""
    if(comment.id not in already_done and str(comment.author) != "artcbot"):
        #marking comment as read if it's a reply
        #this ensures that the PM part does not respond as well
        comment.mark_read()
        already_done.append(comment.id)
        #Making sure the already_done file doesn't get too big. 
        del already_done[0]
        artcbot.write_out("already_done",already_done)

        #Saving comment
        comment_list = str(comment.body)
        comment_list = comment_list.split(' ')

        #passing off to get reply
        reply = artcbot.call_bot(comment_list, comment.author, contributors)

        #Responding if needed
        if(len(reply) > 1):
            reply += "\n\n---\n\n^^To ^^cut ^^down ^^on ^^spam ^^you ^^can ^^private ^^message ^^me ^^commands."
            comment.reply(reply)

#sorting through unread messages
for pm in r.inbox.unread(limit=25):
    pm.mark_read()
    #only responding to pm's, not comment replies
    if(not pm.was_comment):
        body = str(pm.body)
        body = body.split(' ')

        reply = artcbot.call_bot(body, pm.author, contributors)

    #Responding
    if(len(reply) > 1):
        pm.author.message(pm.subject, reply)